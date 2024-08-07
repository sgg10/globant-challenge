from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import APISettings
from app.core.constants import DATABASE_CONNECTION_ERROR


def create_session():
    """
    Create a connection to the database and return the engine and session objects.

    Returns:
        - engine: sqlalchemy.engine.base.Connection
        - session: sqlalchemy.orm.session.Session
    """

    DB_HOST = APISettings.DATABASE["HOST"]
    DB_NAME = APISettings.DATABASE["NAME"]
    DB_USER = APISettings.DATABASE["USER"]
    DB_PASS = APISettings.DATABASE["PASSWORD"]

    try:
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        return engine, Session()
    except Exception as e:
        print(f"{DATABASE_CONNECTION_ERROR}: {e}")
        return None, None
