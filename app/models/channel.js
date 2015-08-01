import Ember from 'ember';
import shortid from 'npm:shortid';

var ivSeparator = '|';

export default Ember.Object.extend({
  id: null,

  init: function () {
    if (!this.id) {
      this.id = shortid.generate();
      this.salt = forge.random.getBytesSync(128);
      this.password = shortid.generate();
    }

    this.id_b64 = forge.util.encode64(this.id);
    this.key = forge.pkcs5.pbkdf2(this.password, this.salt, 32, 32);
  },

  encrypt: function (str) {
    var iv = forge.random.getBytesSync(32),
        cipher = forge.aes.startEncrypting(this.key, iv),
        input = forge.util.createBuffer(str);
    cipher.update(input);
    cipher.finish();
    return [this.id, iv, cipher.output.data].
      map(forge.util.encode64).
      join(ivSeparator);
  },

  decrypt: function (str) {
    if (str.indexOf(this.id_b64) !== 0) {
      return str;
    }

    var byteArray = str.split(ivSeparator).map(forge.util.decode64),
        iv = byteArray[1],
        text = byteArray[2],
        ptext = forge.aes.startDecrypting(this.key, iv),
        newBuffer = forge.util.createBuffer(text);
    ptext.update(newBuffer);
    ptext.finish();
    return ptext.output.data;
  }
});
