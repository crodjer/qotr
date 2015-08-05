import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';


moduleForComponent('scroll-to-bottom', 'Integration | Component | scroll to bottom', {
  integration: true
});

test('it renders', function(assert) {
  assert.expect(2);

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{scroll-to-bottom}}`);

  assert.equal(this.$().text(), '');

  // Template block usage:
  this.render(hbs`
    {{#scroll-to-bottom}}
      template block text
    {{/scroll-to-bottom}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
