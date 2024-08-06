#!/bin/bash

export PGPASSWORD=$POSTGRES_PASSWORD
export PGUSER=$POSTGRES_USER

# Function to validate if the table passed as parameter exists
table_exists() {
    psql -h $POSTGRES_HOST -d $POSTGRES_DB -c "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '$1');" | grep -q 't'
}

# Wait for the database to be ready
until pg_isready -h $POSTGRES_HOST -p 5432; do
    echo "Waiting for the database to be ready..."
    sleep 60
done

# Validate if the specified tables exist
tables=(
    "employee"
    "department"
    "job"
    "task"
    "task_status"
    "task_type"
)

for table in "${tables[@]}"
do
    until table_exists $table; do
        echo "Waiting for the table $table to be ready..."
        sleep 2
    done
done

echo "All tables are ready. Starting the migration script..."
python main.py
