/*
* Crea tabella per citazioni con foreign key id articolo (relazione many to one)
* */
export async function up(knex) {
  if (await knex.schema.hasTable('quotes')) return;
  return knex.schema.createTable('quotes', (table) => {
    table.increments('id');
    table.string('source').notNullable();
    table.string('description');
    table.integer('article_id').unsigned().references('id').inTable('articles').onDelete('CASCADE');
    table.datetime('created_at').defaultTo(knex.fn.now());
  });
}

export function down(knex) {
  return knex.schema.dropTableIfExists('quotes');
}
