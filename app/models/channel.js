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

export default Ember.Object.extend({
  id: null,
  id_b64: null,
  nick: null,
  salt: null,
  password: null,
  socket: null,
  members: null,
  messages: null,

  init: function () {
    if (!this.id) {
      this.set('id', shortid.generate());
      this.set('salt', forge.random.getBytesSync(128));
      this.set('password', shortid.generate());
    }

    this.id_b64 = e64(this.id);
    this.members = Ember.A();
    this.messages = Ember.A();

    if (!this.get('nick')) {
      this.set('nick', shortid.generate());
    }
  },

  key: Ember.computed('salt', 'password', function () {
    return forge.pkcs5.pbkdf2(this.get('password'), this.get('salt'), 32, 32);
  }),

  start: function () {
    return Ember.$.post(httpPrefix + '/c/new', {
      id: this.id,
      salt: e64(this.salt),
      key_hash: this.get('key_hash')
    });
  },

  connect: function () {
    var socket = new WebSocket(wsPrefix + '/c/' + this.id),
        _this = this;
    this.socket = socket;
    this.socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        if (message.sender === null) {
          _this.onServerMessage(message);
        } else {
          _this.onFriendMessage(message);
    }};
  },

  encrypt: function (str) {
    var iv = forge.random.getBytesSync(32),
        cipher = forge.aes.startEncrypting(this.get('key'), iv),
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
        ptext = forge.aes.startDecrypting(this.get('key'), iv),
        newBuffer = forge.util.createBuffer(text);

    ptext.update(newBuffer);
    ptext.finish();
    return ptext.output.data;
  },

  send: function (kind, body) {
    if (body !== null) {
      body = this.encrypt(body);
    }
    this.socket.send(JSON.stringify({
      kind: kind,
      body: body
    }));
  },

  onServerMessage: function (message) {
    var that = this;

    switch(message.kind) {
    case "salt":
      this.set('salt', d64(message.body));
      this.send('join', this.get('nick'));
      Ember.run.later(function () {
        that.send('members');
      });
      break;
    case "members":
      this.set('members', Ember.A(message.body.map(function (nick) {
        return that.decrypt(nick);
      })));
      break;
    case "error":
      console.log("Error: " + message.body);
      break;
    }
  },

  onFriendMessage: function (/* message */) {
  },
});
