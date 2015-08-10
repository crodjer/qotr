/* global require, module, process */
var EmberApp = require('ember-cli/lib/broccoli/ember-app'),
    cdnPrefix = process.env.CDN_PREFIX || '',
    isProduction = EmberApp.env() === 'production';

function styleTag (cdnUrl) {
  return '<link rel="stylesheet" href="' + cdnUrl + '">';
}

function scriptTag (cdnUrl) {
  return '<script src="' + cdnUrl +'"></script>';
}

module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
    fingerprint: {
      prepend: cdnPrefix
    },
    vendorFiles: isProduction ? {
      'handlebars.js': false,
      'ember.js': false,
      'jquery.js': false
    } : {},
    inlineContent: isProduction ? {
      'public-cdn-css': {
        content: [
          '//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css'
        ].map(styleTag).join('\n')
      },
      'public-cdn-js': {
        content: [
          '//ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js',
          '//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js',
          '//cdnjs.cloudflare.com/ajax/libs/handlebars.js/3.0.3/handlebars.min.js',
          '//cdnjs.cloudflare.com/ajax/libs/ember.js/1.13.7/ember.min.js'
        ].map(scriptTag).join('\n')
      }
    } : {}
  });

  if (!isProduction) {
    app.import('bower_components/bootstrap/dist/js/bootstrap.js');
    app.import('bower_components/bootstrap/dist/css/bootstrap.css');
    app.import('bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff', {
      destDir: 'fonts'
    });
    app.import('bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2', {
      destDir: 'fonts'
    });
  }

  app.import('vendor/forge.min.js');
  app.import('vendor/regex-weburl.js');
  return app.toTree();
};
