import Ember from 'ember';
import shortid from 'npm:shortid';
import config from '../config/environment';
import InvalidEncryptionError from '../utils/invalid-encryption-error';

var ivSeparator = '|',
    OUT = { direction: "out" },
    IN = { direction: "in" },
    mayBeUnsafe = ' is not encrypted (or properly encrypted). ' +
      'Continuing this chat is not safe.';

var host = window.location.hostname,
    protocolSuffix = window.location.protocol.replace(/^http/, '') + '//',
    port = config.QOTR_PORT ? ':' + config.QOTR_PORT : '',
    hostTemplate = protocolSuffix + host + port,
    wsPrefix = 'ws' + hostTemplate,
    httpPrefix = 'http' + hostTemplate;

var e64 = forge.util.encode64,
    d64 = forge.util.decode64;

function mkMessage() {
  var message = Ember.Object.create.apply(Ember.Object, arguments);
  message['is' + Ember.String.capitalize(message.kind)] = true;

  return message;
}

export default Ember.Object.extend({
  id: null,
  member_id: null,
  nick: null,
  salt: null,
  password: null,
  socket: null,
  members: null,
  messages: null,
  connected: false,

  init: function () {
    if (!this.id) {
      this.set('id', shortid.generate());
      this.set('salt', forge.random.getBytesSync(128));
      this.set('password', shortid.generate());
    }

    this.set('members', {});
    this.set('messages', Ember.A());

    if (!this.get('nick')) {
      this.set('nick', shortid.generate());
    }
  },

  key: Ember.computed('salt', 'password', function () {
    return forge.pkcs5.pbkdf2(this.get('password'), this.get('salt'), 32, 32);
  }),

  start: function () {
    return Ember.$.post(httpPrefix + '/channels/new', {
      id: this.id,
      meta: e64(this.salt)
    });
  },

  connect: function () {
    var socket = new WebSocket(wsPrefix + '/channels/' + this.id),
        that = this;
    this.socket = socket;
    function setConnected () {
      that.set('connected', socket.readyState === 1);
    }
    this.socket.onopen = setConnected;
    this.socket.onclose = setConnected;
    this.socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        if (message.sender === null) {
          that.onServerMessage(message);
        } else {
          that.onFriendMessage(message);
        }
    };

    this.pingInterval = setInterval(function () {
      that.send('ping');
    }, 30000);
  },

  disconnect: function () {
    clearInterval(this.pingInterval);

    this.socket.close();
    delete this.socket;
  },

  ivHmac: function (iv) {
    var _hmac = forge.hmac.create();
    _hmac.start('sha256', this.get('key'));
    _hmac.update(iv);
    return _hmac.digest().toHex();
  },

  encrypt: function (str) {
    var iv = forge.random.getBytesSync(32),
        cipher = forge.aes.startEncrypting(this.get('key'), iv),
        input = forge.util.createBuffer(str);
    cipher.update(input);
    cipher.finish();
    return [this.ivHmac(iv), iv, cipher.output.data].map(e64).join(ivSeparator);
  },

  decrypt: function (str) {
    var byteArray = str.split(ivSeparator).map(d64),
        ivHmac = byteArray[0] || '',
        iv = byteArray[1] || '',
        text = byteArray[2] || '',
        ptext = forge.aes.startDecrypting(this.get('key'), iv),
        newBuffer = forge.util.createBuffer(text);

    if (ivHmac !== this.ivHmac(iv) ){
      throw new InvalidEncryptionError();
    }

    ptext.update(newBuffer);
    ptext.finish();
    return ptext.output.data;
  },

  send: function (kind, body) {
    var message = {
      kind: kind,
      body: body
    };
    if (kind === 'chat') {
      this.messages.pushObject(mkMessage(message, OUT, { sender: "Me" }));
    }
    if (body !== null) {
      message.body = this.encrypt(message.body);
    }
    this.socket.send(JSON.stringify(message));
  },

  onServerMessage: function (message) {
    var that = this,
        body = message.body;

    switch(message.kind) {
    case "config":
      this.set('salt', d64(body.meta));
      this.set('member_id', body.id);
      this.send('join', this.get('nick'));
      break;
    case "join":
      that.send('members');
      break;
    case "members":
      var members = {};
      Object.keys(body).forEach(function (id) {
        try {
          members[id] = that.decrypt(body[id]);
        } catch (e) {
          if (e instanceof InvalidEncryptionError) {
            members[id] = body[id];
            that.messages.pushObject(mkMessage({
              'kind': 'error',
              'body': 'Nick: ' + body[id] + mayBeUnsafe
            }, IN));
          } else {
            throw e;
          }
        }
      });

      this.set('members', members);
      break;
    case "pong":
      break;
    case "error":
      this.messages.pushObject(mkMessage(message, IN));
      break;
    }
  },

  onFriendMessage: function (message) {
    var members = this.get('members');
    message.sender = members[message.sender] || message.sender;

    if (message.body) {
      try {
        message.body = this.decrypt(message.body);
      } catch (e) {
        if (e instanceof InvalidEncryptionError) {
          this.messages.pushObject(mkMessage({
            'kind': 'error',
            'body': 'A message from ' + message.sender + mayBeUnsafe
          }, IN));
        } else {
          throw e;
        }
      }
    }

    switch(message.kind) {
    case "join":
      this.send('members');
      message.sender = message.body;
      this.messages.pushObject(mkMessage(message, IN));
      break;
    case "part":
      this.send('members');
      this.messages.pushObject(mkMessage(message, IN));
      break;
    case "chat":
      this.messages.pushObject(mkMessage(message, IN));
      break;
    case "nick":
      this.messages.pushObject(mkMessage(message, {
        oldNick: message.sender,
        newNick: message.body
      }, IN));
      this.send('members');
      break;
    case "error":
      this.messages.pushObject(mkMessage(message, IN));
      break;
    }
  }
});
