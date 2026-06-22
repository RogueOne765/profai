/*
* Crea tabella per autori
* */
export async function up(knex) {
  if (await knex.schema.hasTable('authors')) return;
  return knex.schema.createTable('authors', (table) => {
    table.increments('id');
    table.string('name').notNullable();
    table.string('surname').notNullable();
    table.datetime('created_at').defaultTo(knex.fn.now());
  });
}

export function down(knex) {
  return knex.schema.dropTableIfExists('authors');
}
