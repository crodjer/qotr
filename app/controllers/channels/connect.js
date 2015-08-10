import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    editNick: function () {
      this.set('editingNickText', this.get('model.nick'));
      this.set('editingNick', true);
    },
    cancelNickEdit: function () {
      this.set('editingNick', false);
    },
    nickSave: function () {
      var that = this,
          nick = this.get('editingNickText').trim(),
          oldNick = this.get('model.nick').trim();

      if (!nick || nick === oldNick) {
        that.set('editingNick', false);
        return;
      }

      if (this.get('makeDefaultNick')) {
        localStorage['qotr-nick'] = nick;
      }

      this.model.set('nick', nick);
      this.model.send('nick', nick);
      Ember.run.later(function () {
        that.model.send('members');
        that.set('editingNick', false);
      }, 200);
    },

    sendChat: function () {
      var text = this.get('chatMessage').trim();
      if (text) {
        this.model.send('chat', text);
      }
      this.set('chatMessage', null);
    },

    connect: function () {
      this.model.connect();
    },

    disconnect: function () {
      this.model.disconnect();
    }
  },

  chataMessage: null,
  makeDefaultNick: false,
  editingNickText: null,
  editingNick: false,
  focused: true,
  pending: 0,

  disabled: Ember.computed('model.connected', function () {
    return !this.get('model.connected');
  }),

  onMessage: Ember.observer('model.messages.[]', function () {
    var messages = this.get('model.messages'),
        lastMessage = messages[messages.length - 1];

    if (!this.get('focused') && lastMessage) {
      this.set('pending', this.get('pending') + 1);
    }
  }),

  onPendingChange: Ember.observer('pending', function () {
    var pending = this.get('pending'),
        title = document.title.replace(/^\(\d+\)/, '');
    if (pending > 0) {
      title = `(${pending}) ` + title;
    }

    document.title = title;
  }),

  onFocusChange: Ember.observer('focused', function () {
    if (this.get('focused')) {
      this.set('pending', 0);
    }
  })
});
