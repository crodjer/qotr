import { moduleFor, test } from 'ember-qunit';
import shortid from 'npm:shortid';

moduleFor('model:channel', 'Unit | Model | channel', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it can be created', function(assert) {
  var channel = this.subject();
  assert.ok(channel.salt);
  assert.ok(channel.password);
  assert.ok(channel.key);
  assert.equal(channel.decrypt(channel.encrypt('foo')), 'foo');
});

test('it can be loaded', function(assert) {
  var obj = {
      id: shortid.generate(),
      salt: forge.random.getBytesSync(128),
      password: shortid.generate()
  };
  var channel = this.subject(obj);

  assert.equal(obj.id, channel.id);
  assert.equal(obj.salt, channel.salt);
  assert.equal(obj.password, channel.password);
  assert.equal(channel.decrypt(channel.encrypt('foo')), 'foo');
});

test('it ignores text which isn\'t encrypted', function(assert) {
  var channel = this.subject();
  assert.equal(channel.decrypt('foo'), 'foo');
});
