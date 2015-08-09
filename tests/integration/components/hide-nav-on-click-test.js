import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';


moduleForComponent('hide-nav-on-click', 'Integration | Component | hide nav on click', {
  integration: true
});

test('it renders', function(assert) {
  assert.expect(2);

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{hide-nav-on-click}}`);

  assert.equal(this.$().text(), '');

  // Template block usage:
  this.render(hbs`
    {{#hide-nav-on-click}}
      template block text
    {{/hide-nav-on-click}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
