import { moduleFor, test } from 'ember-qunit';
import shortid from 'npm:shortid';

moduleFor('model:channel', 'Unit | Model | channel', {
  // Specify the other units that are required for this test.
  needs: []
});

var e64 = forge.util.encode64;

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
      salt: e64(forge.random.getBytesSync(128)),
      password: shortid.generate()
  };
  var channel = this.subject(obj);

  assert.equal(obj.id, channel.id);
  assert.equal(obj.salt, e64(channel.salt));
  assert.equal(obj.password, channel.password);
  assert.equal(channel.decrypt(channel.encrypt('foo')), 'foo');
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
