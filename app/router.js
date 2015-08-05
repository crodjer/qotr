import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('home', { path: "/" });
  this.resource('channels', { path: "/c/"}, function() {
    this.route('new', { path: "/new"});
    this.route('connect', { path: "/:id"});
  });
  this.route('terms-and-conditions');
});

export default Router;
