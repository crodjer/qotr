import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.resource('channels', { path: "/c/"}, function() {
    this.route('new', { path: "/new"});
    this.route('connect', { path: "/:id"});
  });
});

export default Router;
