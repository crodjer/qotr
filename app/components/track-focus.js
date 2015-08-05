import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement: function () {
    var that = this,
        winEl = Ember.$(window);

    winEl.focus(function () {
      that.set('focused', true);
    });

    winEl.focusout(function () {
      that.set('focused', false);
    });
  }
});
