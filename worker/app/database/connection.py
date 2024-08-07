from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import constants


def create_session():
    """
    Create a connection to the database and return the engine and session objects.

    Returns:
        - engine: sqlalchemy.engine.base.Connection
        - session: sqlalchemy.orm.session.Session
    """

    DB_HOST = constants.DB_HOST
    DB_NAME = constants.DB_NAME
    DB_USER = constants.DB_USER
    DB_PASS = constants.DB_PASS

    try:
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        return engine, Session()
    except Exception as e:
        print(f"{constants.DATABASE_CONNECTION_ERROR}: {e}")
        return None, None
