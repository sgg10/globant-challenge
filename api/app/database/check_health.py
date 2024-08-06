from sqlalchemy import text

from app.database.connection import create_session
from app.core.constants import DATABASE_CHECK_HEALTH_ERROR, DATABASE_CHECK_HEALTH_QUERY


def check_database_health():
    """
    Checks the health of the database.

    Returns:
        tuple: A tuple containing a boolean value indicating the health status of the database (True if healthy, False otherwise) and a message string.
    """

    try:
        engine, session = create_session()

        with engine.connect() as connection:
            _ = connection.execute(text(DATABASE_CHECK_HEALTH_QUERY))

        session.close()
        return True, ""
    except Exception as e:
        message = f"{DATABASE_CHECK_HEALTH_ERROR}: {e}"
        return False, message
