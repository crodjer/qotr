import Ember from 'ember';

import lineBreaks from '../utils/line-breaks';
import tagUrls from '../utils/tag-urls';

var processors = [
  lineBreaks,
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
