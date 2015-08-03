import Ember from 'ember';
import { moduleFor, test } from 'ember-qunit';
import shortid from 'npm:shortid';

moduleFor('model:channel', 'Unit | Model | channel', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it can be created', function(assert) {
  var channel = this.subject();

  assert.ok(channel.get('salt'));
  assert.ok(channel.get('password'));
  assert.ok(channel.get('key'));
  assert.ok(channel.get('key_hash'));
  assert.equal(channel.decrypt(channel.encrypt('foo')), 'foo');
});

test('it can be loaded', function(assert) {
  var obj = {
      id: shortid.generate(),
      password: shortid.generate()
  };
  var salt = forge.random.getBytesSync(128);

  var channel = this.subject(obj);
  channel.set('salt', salt);

  Ember.run.later(function () {
    assert.equal(channel.id, obj.id);
    assert.equal(channel.get('salt'), salt);
    assert.equal(channel.get('password'), obj.password);
    assert.equal(channel.decrypt(channel.encrypt('foo')), 'foo');
  }, 100);
});

test('it ignores text which isn\'t encrypted', function(assert) {
  var channel = this.subject();
  assert.equal(channel.decrypt('foo'), 'foo');
});

test('it creates a actual channel on server', function(assert) {
  var channel = this.subject();
  channel.create().then(function(resp) {
    assert.equal(channel.id, resp.id);
  });
});

test('it connects to the server', function(assert) {
  var channel = this.subject();
  channel.create().then(function(/* response */) {
    channel.connect();
    assert.ok(channel.socket);
    assert.ok(channel.socket.readyState < channel.socket.CLOSING);
  });
});
