
# globant-challenge

This repository contains the solution to the challenge proposed by Globant. The design of the solution is divided into 3 diagrams that can be found in the `architecture.drawio` file. The idea of this challenge was to separate each of the key components of the challenge and focused on not having an API that received the data and was in charge of uploading it to the database, but rather having an API layer that could receive requests and create independent tasks that will be resolved by one or more workers, who will manage all the operations requested in the challenge.

The idea of approaching the challenge in this way is to generate greater scalability and not have to depend on an API service that could be stressed by receiving a large number of requests (considering that we are talking about Big Data, I consider it important to take care of this aspect), also to have better control of the tasks that are being executed, in addition to having better control of the errors that may occur in the task execution process.

The communication between API and workers was carried out through Apache Kafka, which is responsible for managing the messages sent between the different components of the solution.

This repository contains 5 directories, which represent each part of the challenge, described below:

1. **database**: In this directory, you will find the definition of the database used for the challenge, its initial values were assigned and it was managed with `Liquibase` to have better control of the changes made to the database.
2. **api**: In this directory, you will find the definition of the API that is responsible for receiving requests and sending them to the workers for processing. Since we are talking about a task model, it has its respective endpoint to query the status of the tasks that have been sent to the workers. This API was developed with `FastAPI`.
3. **workers**: This directory contains the definition of the workers that are responsible for processing the tasks that are sent from the API. Each worker has its definition and the necessary logic to be able to process the tasks independently. These workers were developed in `Python` and `Celery`.
4. **kafka**: This directory contains the necessary configuration to be able to lift an instance of Apache Kafka locally, which will be in charge of managing the messages sent between the API and the workers.
5. **scripts**: This directory contains a series of scripts that are responsible for automating certain tasks within the solution. It includes the script `up.sh` which is responsible for lifting the entire solution locally and the script `down.sh` which is responsible for bringing down the solution and cleaning up the environment.

## Solution Architecture

The solution architecture can be found in the `architecture.drawio` file, which contains three diagrams: a general diagram of the solution, a diagram of the API, and a diagram of the workers. Below is a description of each of them:

- **General Diagram**: This diagram shows the general flow of the solution, from the moment the request is received by the API until it is processed by the workers and the result is stored in the database.
- **API Diagram**: This diagram shows the internal architecture of the API, including the different endpoints that have been defined and the flow of requests within the API.
- **Workers Diagram**: This diagram shows the internal architecture of the workers, including the different tasks that have been defined and the flow of messages between the workers and the API.

## Steps to Deploy the Solution

1. Clone the repository
2. Refer to the `.env.example` file and create a `.env` file with the necessary environment variables for the solution's execution. AWS keys are requested to be able to connect with the S3 service; you can use the keys provided to recruiter for testing purposes (permissions are only granted for the bucket used in the challenge).
3. Run the `up.sh` script to lift and prepare the solution's execution environment. This script will replace environment variables at key points in the files where required to maintain the solution's configuration, then it will lift the necessary containers with `Docker Compose`, define the database with `Liquibase`, and run the data migration script (one minute after lifting the containers), finally creating the Kafka topic to manage messages between the API and the workers.

## Usage

Once the `up.sh` script has been executed, you can access the API at `http://localhost:8888/docs` (or the port defined in the `.env` file) and view the API documentation and perform the necessary tests to send tasks to the workers.

## Points of Improvement

- A schema registry can be used to have better control of the messages sent between the API and the workers. This would involve lifting another service and establishing the schemas of the messages sent between the components.
- The solution can be deployed on an ECS cluster in AWS to have better scalability and availability of the solution, and clearly, so that it does not have to be deployed in a local environment (the goal of this challenge was to be able to deploy to AWS in an ECS cluster with Terraform and pipelines in Github to make the Docker images available, but due to time constraints, it was not possible to do so).
