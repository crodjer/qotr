import Ember from 'ember';
import Channel from '../models/channel';

export default Ember.Route.extend({
  model: function (params) {
    var channel = Channel.create({
      id: params.channel_id,
      password: location.hash.replace(/^#/, ''),
      nick: localStorage['qotr-nick']
    });
    channel.connect();

    return channel;
  }
});
