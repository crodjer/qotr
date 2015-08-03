import { moduleFor, test } from 'ember-qunit';

moduleFor('model:channel', 'Unit | Model | channel', {
});

test('it can be created', function(assert) {
  var channel = this.factory().create();

  assert.ok(channel.get('salt'));
  assert.ok(channel.get('password'));
  assert.ok(channel.get('key'));
  assert.ok(channel.get('key_hash'));
  assert.equal(channel.decrypt(channel.encrypt('foo')), 'foo');
});

test('it ignores text which isn\'t encrypted', function(assert) {
  var channel = this.factory().create();
  assert.equal(channel.decrypt('foo'), 'foo');
});

test('it creates an actual channel on server', function(assert) {
  var channel = this.factory().create();
  channel.start().then(function(resp) {
    assert.equal(channel.id, resp.id);
  });
});

test('it can load a channel', function(assert) {
  var factory = this.factory();

  var config = {
    id: 'test-channel',
    password: 'foo'
  };
  var channel = factory.create(config);
  assert.equal(channel.id, config.id);
  assert.equal(channel.password, config.password);
  assert.ok(!channel.salt);
});

test('it connects to a existing channel correctly', function(assert) {
  var factory = this.factory(),
      creator = factory.create();

  creator.start().then(function(resp) {
    var channel = factory.create({
      id: resp.id,
      password: creator.password
    });
    channel.connect();

    assert.ok(!channel.salt);
    assert.equal(channel.id, resp.id);

    function onSalt () {
        var str = 'foo';

        assert.equal(channel.get('salt'), creator.get('salt'));
        assert.equal(channel.get('password'), creator.get('password'));
        assert.equal(channel.get('key'), creator.get('key'));
        assert.equal(channel.id, creator.id);
        assert.equal(channel.id_b64, creator.id_b64);

        var encrypted = creator.encrypt(str);
        assert.notEqual(encrypted, str);
        assert.equal(channel.decrypt(creator.encrypt(str)), str);
      }

    channel.addObserver('salt', onSalt);
  });
});
