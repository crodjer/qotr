import Ember from 'ember';
import shortid from 'npm:shortid';
import config from '../config/environment';

var ivSeparator = '|';

var host = window.location.hostname,
    protocolSuffix = window.location.protocol.replace(/^http/, '') + '//',
    port = config.QOTR_PORT ? ':' + config.QOTR_PORT : '',
    hostTemplate = protocolSuffix + host + port,
    wsPrefix = 'ws' + hostTemplate,
    httpPrefix = 'http' + hostTemplate;

var e64 = forge.util.encode64,
    d64 = forge.util.decode64;

function hmac (str) {
    var _hmac = forge.hmac.create();
    _hmac.start('sha256', str);
    return _hmac.digest().toHex();
}

export default Ember.Object.extend({
  id: null,
  socket: null,

  init: function () {
    if (this.id) {
      this.salt = d64(this.salt);
    } else {
      this.id = shortid.generate();
      this.salt = forge.random.getBytesSync(128);
      this.password = shortid.generate();
    }

    this.id_b64 = e64(this.id);
    this.key = forge.pkcs5.pbkdf2(this.password, this.salt, 32, 32);
    this.key_hash = hmac(this.key);
  },

  create: function () {
    return Ember.$.post(httpPrefix + '/c/new', {
      id: this.id,
      salt: e64(this.salt),
      key_hash: this.key_hash
    });
  },

  connect: function () {
    this.socket = new WebSocket(wsPrefix + '/c/' + this.id);
  },

  encrypt: function (str) {
    var iv = forge.random.getBytesSync(32),
        cipher = forge.aes.startEncrypting(this.key, iv),
        input = forge.util.createBuffer(str);
    cipher.update(input);
    cipher.finish();
    return [this.id, iv, cipher.output.data].map(e64).join(ivSeparator);
  },

  decrypt: function (str) {
    if (str.indexOf(this.id_b64) !== 0) {
      return str;
    }

    var byteArray = str.split(ivSeparator).map(d64),
        iv = byteArray[1],
        text = byteArray[2],
        ptext = forge.aes.startDecrypting(this.key, iv),
        newBuffer = forge.util.createBuffer(text);
    ptext.update(newBuffer);
    ptext.finish();
    return ptext.output.data;
  }
});
