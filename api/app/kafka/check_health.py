from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient

from app.core.settings import APISettings
from app.core.constants import (
    KAFKA_CHECK_HEALTH_SUCCESS,
    KAFKA_CHECK_HEALTH_ERROR,
    KAFKA_CHECK_HEALTH_NO_EXISTS_TOPIC_ERROR,
)


def create_kafka_admin_client(bootstrap_servers):
    """
    Creates a Kafka admin client.

    Parameters:
    - bootstrap_servers (str): The bootstrap servers for the Kafka cluster.

    Returns:
    - AdminClient: The Kafka admin client.

    """
    return AdminClient({"bootstrap.servers": bootstrap_servers})


def check_kafka_health():
    """
    Check the health of the Kafka cluster.

    Returns:
        tuple: A tuple containing a boolean value indicating the health status and a string message.
            - If the Kafka topic exists in the cluster, the health status is True and the message is KAFKA_CHECK_HEALTH_SUCCESS.
            - If the Kafka topic does not exist in the cluster, the health status is False and the message is KAFKA_CHECK_HEALTH_NO_EXISTS_TOPIC_ERROR.
            - If an exception occurs during the health check, the health status is False and the message is KAFKA_CHECK_HEALTH_ERROR followed by the exception message.
    """
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
