from uuid import uuid4
from confluent_kafka import Producer

from app.core.settings import APISettings


def get_kafka_producer():
    """
    Returns a Kafka producer with the following configuration:
        - bootstrap.servers: The host and port of the Kafka server.
        - enable.idempotence: Enables idempotent producer behavior.
        - transactional.id: A unique identifier for the transactional producer.

    Returns:
        Producer: A Kafka producer object.
    """
    return Producer(
        {
            "bootstrap.servers": f"{APISettings.KAFKA['HOST']}:{APISettings.KAFKA['PORT']}",
            "enable.idempotence": True,
            "transactional.id": str(uuid4()),
        }
    )
