#!/bin/bash

filter="${1}*.sql"

files=`ls $filter 2>/dev/null`
[[ -n $files ]] || { echo "No migrations found."; exit 1; }

for f in $files; do
  if [ "`mysql -u root -D easynutdata -B -N -e "SELECT COUNT(*) FROM sql_migrations WHERE name='${f%.*}'" 2>&1`" != "1" ]; then
    echo "Applying $f..."
    mysql -u root < "$f"
  fi
done
