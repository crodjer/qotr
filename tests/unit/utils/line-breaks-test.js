import lineBreaks from '../../../utils/line-breaks';
import { module, test } from 'qunit';

module('Unit | Utility | line breaks');

test('it does not touch normal messages', function(assert) {
  var string = 'foo bar',
      result = lineBreaks(string);
  assert.equal(result, string);
});

test('it replaces newlines to line breaks', function(assert) {
  var result = lineBreaks('foo\nbar');
  assert.equal(result, 'foo<br/>bar');
});
