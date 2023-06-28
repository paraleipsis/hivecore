#!/usr/bin/env sh

KAFKA_HOST=$(yq eval '.KAFKA_HOST' configs/storage_config.yml)
KAFKA_PORT=$(yq eval '.KAFKA_PORT' configs/storage_config.yml)
./wait-for-it.sh --timeout=0 -s "$KAFKA_HOST":"$KAFKA_PORT"

DB_HOST=$(yq eval '.DB_HOST' configs/storage_config.yml)
DB_PORT=$(yq eval '.DB_PORT' configs/storage_config.yml)
./wait-for-it.sh --timeout=0 -s "$DB_HOST":"$DB_PORT"

alembic revision --autogenerate -m 'database creation'
alembic upgrade head

python3 src/cli/main.py ssh-keys
python3 src/cli/main.py secret-key --write
python3 src/cli/main.py db-init-models

python3 src/core/hivecore.py
