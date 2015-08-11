import tagUrls from '../../../utils/tag-urls';
import { module, test } from 'qunit';

module('Unit | Utility | tag urls');

test('it does not modify a message without url', function(assert) {
  var message = 'foo bar baz',
      result = tagUrls(message);
  assert.equal(result, message);
});

test('it converts urls into anchor tag', function(assert) {
  var message = 'foo http://www.google.com',
      result = tagUrls(message);
  assert.ok(/^foo <a.*?href=/.exec(result));
});
