import Ember from 'ember';
import Channel from '../../models/channel';

export default Ember.Route.extend({
  actions: {
    willTransition: function() {
      this.currentModel.disconnect();
    }
  },

  model: function (params) {
    var channel = Channel.create({
      id: params.id,
      password: location.hash.replace(/^#/, ''),
      nick: localStorage['qotr-nick']
    });
    channel.connect();

    return channel;
  }
});
