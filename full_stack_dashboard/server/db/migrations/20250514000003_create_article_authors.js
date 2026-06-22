/*
* Crea tabella bridge tra autori e articoli (relazione many to many)
* */
export async function up(knex) {
  if (await knex.schema.hasTable('article_authors')) return;
  return knex.schema.createTable('article_authors', (table) => {
    table.integer('article_id').unsigned().notNullable().references('id').inTable('articles').onDelete('CASCADE');
    table.integer('author_id').unsigned().notNullable().references('id').inTable('authors').onDelete('CASCADE');
    table.primary(['article_id', 'author_id']);
  });
}

export function down(knex) {
  return knex.schema.dropTableIfExists('article_authors');
}
