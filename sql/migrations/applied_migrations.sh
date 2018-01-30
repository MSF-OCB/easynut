#!/bin/sh

[ -n "$1" ] && LIMIT="LIMIT $1" || LIMIT=""

mysql -u root -p$MYSQL_ROOT_PASSWORD -D easynutdata -e "SELECT * FROM sql_migrations ORDER BY applied DESC, _id DESC $LIMIT"
