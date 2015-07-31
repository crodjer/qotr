import { moduleFor, test } from 'ember-qunit';

moduleFor('model:channel', 'Unit | Model | channel', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it can be created', function(assert) {
  var channel = this.subject({
    id: 'foo'
  });

  assert.equal(channel.id, 'foo');
});
