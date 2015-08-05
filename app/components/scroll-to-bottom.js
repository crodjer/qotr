import Ember from 'ember';

export default Ember.Component.extend({
  scrollToBottom: Ember.observer('items.@each', function () {
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
