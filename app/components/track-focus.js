import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement: function () {
    var winEl = Ember.$(window),
        that = this;

    this.onFocus = function () {
      that.set('focused', true);
    };

    this.onFocusOut = function () {
      that.set('focused', false);
    };

    winEl.on('focus', this.onFocus);
    winEl.on('focusout', this.onFocusOut);
  },

  willDestroy: function () {
    var winEl = Ember.$(window);

    winEl.off('focus', this.onFocus);
    winEl.off('focusout', this.onFocusOut);
  }
});
