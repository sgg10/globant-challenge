#!/bin/bash

echo "Starting containers..."
docker-compose up -d --build
echo "Containers started."

sleep 10

echo "Creating topics..."
docker-compose exec kafka kafka-topics --bootstrap-server kafka:9092\
    --create --topic globant-challenge --partitions 1 --replication-factor 1 --if-not-exists

echo "Topics created."