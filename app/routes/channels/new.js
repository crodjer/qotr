import Ember from 'ember';
import Channel from '../../models/channel';

export default Ember.Route.extend({
  model: function () {
    var channel = Channel.create({
      nick: localStorage['qotr-nick']
    });

    return channel.start().then(function () {
      channel.connect();

      return channel;
    });
  },

  afterModel: function(channel /*,  transition */) {
    this.transitionTo('channels.connect', channel).then(function () {
      // Set the password as a location hash, to create a shareable link.
      location.hash = channel.get('password');
    });
  }
});
