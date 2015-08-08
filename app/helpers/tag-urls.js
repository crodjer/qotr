/* global re_weburl */
import Ember from 'ember';

function toTag (url) {
  return '<a target="_blank" href="' + url + '">' + url + '</a>';
}

var punctuation = "[\.,]",
    splitRe = new RegExp([
      punctuation + "$",
      punctuation + "\\s+",
      "\\s+",
    ].join('|'));

export default Ember.Handlebars.makeBoundHelper(function(value) {
  var urlMap = {};

  value = Ember.Handlebars.Utils.escapeExpression(value);

  console.log(splitRe.source);
  value.split(splitRe).forEach(function (slice) {
    if (slice.match(re_weburl)) {
      urlMap[slice] = toTag(slice);
    }
  });

  Object.keys(urlMap).forEach(function (url) {
    var source = url,
        tag = urlMap[url];

    value = value.replace(source, tag);
  });

  return new Ember.Handlebars.SafeString(value);
});
