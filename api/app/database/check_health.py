from sqlalchemy import text
from app.database.connection import create_session


def check_database_health():
    """
    Checks the health of the database.

    Returns:
        tuple: A tuple containing a boolean value indicating the health status of the database (True if healthy, False otherwise) and a message string.
    """

    try:
        engine, session = create_session()

        with engine.connect() as connection:
            _ = connection.execute(text("SELECT 1"))

        session.close()
        return True, ""
    except Exception as e:
        message = f"Error checking database health: {e}"
        print(message)
        return False, message
