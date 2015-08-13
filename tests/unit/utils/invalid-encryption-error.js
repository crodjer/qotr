import UnencryptedError from '../../../utils/invalid-encryption-error';
import { module, test } from 'qunit';

module('Unit | Utility | unencrypted error');

// Replace this with your real tests.
test('it works', function(assert) {
  try {
    throw new UnencryptedError();
  } catch (e) {
    assert.ok(e instanceof UnencryptedError);
  }
});
