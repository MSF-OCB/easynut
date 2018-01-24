# EasyNut SQL Migrations

- List all applied migrations: `./applied_migrations.sh`
- List last 5 applied migrations: `./applied_migrations.sh 5`

- Apply all migrations: `./migrate.sh`
- Apply a specific migration: `./migrate.sh 0001` (_actually all files matching `0001*.sql`_)
