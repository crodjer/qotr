import Ember from 'ember';

import tagUrls from '../utils/tag-urls';

var processors = [
  tagUrls
];

export function formatMessage(value) {
  value = Ember.Handlebars.Utils.escapeExpression(value);

  processors.forEach(function (processor) {
    value = processor(value);
  });

  return new Ember.Handlebars.SafeString(value);
}

export default Ember.Helper.helper(formatMessage);
