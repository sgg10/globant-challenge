#!/bin/sh

# wait for the database to be ready
until pg_isready -h db -p 5432 -U #!{DATABASE_USER}!#; do
    echo "Waiting for the database to be ready..."
    sleep 1
done

echo "Database is ready. Starting Liquibase..."

liquibase --changelog-file=changelog/changelog-main.yaml \
    --url=jdbc:postgresql://#!{DATABASE_HOST}!#/#!{DATABASE_NAME}!# \
    --username=#!{DATABASE_USER}!# \
    --password=#!{DATABASE_PASSWORD}!# \
    validate

liquibase --changelog-file=changelog/changelog-main.yaml \
    --url=jdbc:postgresql://#!{DATABASE_HOST}!#/#!{DATABASE_NAME}!# \
    --username=#!{DATABASE_USER}!# \
    --password=#!{DATABASE_PASSWORD}!#\
    update

echo "Liquibase has finished. Database is ready!"
