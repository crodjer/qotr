import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement: function () {
    Ember.$('.navbar-collapse').click('.hide-on-click', function() {
      Ember.$('.navbar-collapse').collapse('hide');
    });
  }
});
