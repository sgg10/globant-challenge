import os
import json

from confluent_kafka import Consumer, KafkaException, KafkaError
import constants


def create_consumer():
    """
    Creates a Kafka consumer with the specified configuration.

    Returns:
        Consumer: A Kafka consumer object.

    """

    consumer = Consumer(
        {
            "bootstrap.servers": constants.KAFKA_HOST + ":" + constants.KAFKA_PORT,
            "group.id": constants.KAFKA_GROUP_ID,
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([constants.KAFKA_TOPIC])

    return consumer


def fix_message(message: bytes) -> dict:
    """
    Converts a byte message to a dictionary.

    Args:
        message (bytes): The byte message to be converted.

    Returns:
        dict: The converted dictionary.
    """
    return json.loads(message.value().decode("utf-8"))


def consume(consumer: Consumer):
    """
    Consume messages from a Kafka consumer.

    Args:
        consumer (Consumer): The Kafka consumer to consume messages from.

    Yields:
        The fixed message from the Kafka consumer.

    Raises:
        KafkaException: If there is an error while consuming messages from the Kafka consumer.
    """
    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(message.error())

        yield fix_message(message)
