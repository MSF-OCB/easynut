#!/bin/bash

LIMIT=""
[[ -n $1 ]] && LIMIT="LIMIT $1"

mysql -u root -D easynutdata -e "SELECT * FROM sql_migrations ORDER BY applied DESC, _id DESC $LIMIT"
