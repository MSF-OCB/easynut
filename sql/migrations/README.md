# EasyNut SQL Migrations

## List 5 last applied migrations

```
mysql -u root -D easynutdata -e "SELECT * FROM sql_migrations ORDER BY applied DESC LIMIT 5"
```


# Apply a migration

```
mysql -u root < 0000_initial.sql
```


# Apply all migrations (not yet applied)

```
for f in `ls *.sql`; do [ "`mysql -u root -D easynutdata -B -N -e "SELECT COUNT(*) FROM sql_migrations WHERE name='${f%.*}'" 2>&1`" != "1" ] && { echo "Applying $f..."; mysql -u root < $f; }; done
```
