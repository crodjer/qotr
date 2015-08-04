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
          nick = this.get('editingNickText');

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
    }
  },

  chataMessage: null,
  makeDefaultNick: false,
  editingNickText: null,
  editingNick: false,

  scrollToBottom: Ember.observer('model.messages.@each', function () {
    // A bad hack which scrolls the page to bottom on message push.
    // Possibly better kept at the corresponding view.
    var html = Ember.$('html');

    html.scrollTop(html[0].scrollHeight);
  })
});
