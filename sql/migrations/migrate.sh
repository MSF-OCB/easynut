#!/bin/sh

BASE_DIR="$(cd "$(dirname "${0}")" && pwd)"

filter="${BASE_DIR}/${1}*.sql"

files=`ls $filter 2>/dev/null`
[ -n "$files" ] || { echo "No migrations found."; exit 1; }

for file in $files; do
  filename=`basename $file`
  name="${filename%.*}"
  exists=`mysql -u root -p$MYSQL_ROOT_PASSWORD -D easynutdata -B -N -e "SELECT COUNT(*) FROM sql_migrations WHERE name='$name'" 2>/dev/null`
  if [ "$exists" != "1" ]; then
    echo "Applying $name..."
    mysql -u root -p$MYSQL_ROOT_PASSWORD < "$file"
  fi
done
