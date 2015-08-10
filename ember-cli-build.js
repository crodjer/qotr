/* global require, module, process */
var EmberApp = require('ember-cli/lib/broccoli/ember-app'),
    cdnPrefix = process.env.CDN_PREFIX || '';

module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
    fingerprint: {
      prepend: cdnPrefix
    }
  });

  app.import('bower_components/bootstrap/dist/js/bootstrap.js');
  app.import('bower_components/bootstrap/dist/css/bootstrap.css');
  app.import('bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff', {
    destDir: 'fonts'
  });
  app.import('bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2', {
    destDir: 'fonts'
  });

  app.import('vendor/forge.min.js');
  app.import('vendor/regex-weburl.js');
  return app.toTree();
};
