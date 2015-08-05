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
      this.model.socket.close();
    }
  },

  chataMessage: null,
  makeDefaultNick: false,
  editingNickText: null,
  editingNick: false,

  disabled: Ember.computed('model.connected', function () {
    return !this.get('model.connected');
  }),

  scrollToBottom: Ember.observer('model.messages.@each', function () {
    // A bad hack which scrolls the page to bottom on message push.
    // Possibly better kept at the corresponding view.
    var html = Ember.$('html'),
        body = Ember.$('body');

    Ember.run.later(function () {
      html.scrollTop(html[0].scrollHeight); // Firefox
      body.scrollTop(body[0].scrollHeight); // Chrome
    }, 10);
  })
});
