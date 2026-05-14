export async function up(knex) {
  if (await knex.schema.hasTable('articles')) return;
  return knex.schema.createTable('articles', (table) => {
    table.increments('id');
    table.string('title').notNullable();
    table.text('abstract');
    table.date('publication_date');
    table.string('doi').unique();
    table.datetime('created_at').defaultTo(knex.fn.now());
  });
}

export function down(knex) {
  return knex.schema.dropTableIfExists('articles');
}