#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


if [ "$1" == "-h" ]; then
    echo "$(basename "$0") [-h] [-a s1 -b s2 -d s3 -p s4] -- program to restore a backup file on Scalingo database
where:
    -h  show this help text
    -a  Scalingo app name (required)
    -b  path to backup file
    -d  POSTGRES_URL (required)
    -f  backup file name
    -p  PG_PASSWORD (required)
    -u  PG_USER (required)"
    exit 0
fi

# GET APPLICATION NAME
if [[ $# -gt 1 ]] && [[ "$1" == "-a" ]]; then
  APP_NAME=$2
  shift 2
else
  echo "You must provide a project name."
  exit 1
fi

# PROVIDE BACKUP PATH
if [[ $# -gt 2 ]] && [[ "$1" == "-b" ]]; then
  BACKUP_PATH=$2
  shift 2
else
  BACKUP_PATH=~/$APP_NAME-main/api/db_dumps/
  echo "Using default BACKUP_PATH."
fi

# GET FILE NAME
if [[ $# -gt 1 ]] && [[ "$1" == "-f" ]]; then
  FILE_NAME="$BACKUP_PATH"/$2
  shift 2
else
  FILE_NAME="$BACKUP_PATH"/`date +%Y%m%d_%H%M%S`.pgdump
fi

# GET POSTGRES_URL
if [[ $# -gt 2 ]] && [[ "$1" == "-d" ]]; then
  POSTGRES_URL=$2
  shift 2
else
  echo "You must provide the POSTGRES_URL you want to access."
  exit 1
fi

# GET SCALINGO_PG_PASSWORD
if [[ $# -gt 2 ]] && [[ "$1" == "-p" ]]; then
  PG_PASSWORD=$2
  shift 2
else
  echo "You must provide the SCALINGO_PG_PASSWORD for the database."
  exit 1
fi

# GET SCALINGO_PG_USER
if [[ $# -gt 1 ]] && [[ "$1" == "-u" ]]; then
  PG_USER=$2
  shift 2
else
  echo "You must provide the SCALINGO_PG_USER for the database."
  exit 1
fi

echo "Building tunnel to Scalingo."
scalingo -a "$APP_NAME" db-tunnel "$POSTGRES_URL" &
sleep 3
DB_TUNNEL_PID=$!
echo "Start backup process."
mkdir -p "$BACKUP_PATH"
PGPASSWORD="$PG_PASSWORD" pg_dump --host 127.0.0.1 \
                                  --port 10000 \
                                  --username "$PG_USER" \
                                  --dbname "$PG_USER" -F c > $FILE_NAME
echo "$DB_TUNNEL_PID"
# for some reason kill -2 does not work (network issues maybe)
sudo kill -9 "$DB_TUNNEL_PID"
echo "Database dump: success."
