import Ember from 'ember';

export default Ember.Route.extend({
  model: function (params) {
    return params.channel_id;
  }
});
