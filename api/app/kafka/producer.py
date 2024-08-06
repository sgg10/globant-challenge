from uuid import uuid4
from confluent_kafka import Producer

from app.core.settings import APISettings


def get_kafka_producer():
    return Producer(
        {
            "bootstrap.servers": f"{APISettings.KAFKA['HOST']}:{APISettings.KAFKA['PORT']}",
            "enable.idempotence": True,
            "transactional.id": str(uuid4()),
        }
    )
