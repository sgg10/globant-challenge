from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient

from app.core.settings import APISettings
from app.core.constants import (
    KAFKA_CHECK_HEALTH_SUCCESS,
    KAFKA_CHECK_HEALTH_ERROR,
    KAFKA_CHECK_HEALTH_NO_EXISTS_TOPIC_ERROR,
)


def create_kafka_admin_client(bootstrap_servers):
    return AdminClient({"bootstrap.servers": bootstrap_servers})


def check_kafka_health():
    try:
        admin_client = create_kafka_admin_client(
            f"{APISettings.KAFKA['HOST']}:{APISettings.KAFKA['PORT']}"
        )
        cluster_metadata = admin_client.list_topics(timeout=10)
        if APISettings.KAFKA["TOPIC"] in cluster_metadata.topics:
            return True, KAFKA_CHECK_HEALTH_SUCCESS
        else:
            return False, KAFKA_CHECK_HEALTH_NO_EXISTS_TOPIC_ERROR
    except KafkaException as e:
        return False, f"{KAFKA_CHECK_HEALTH_ERROR}: {e}"
    finally:
        del admin_client
