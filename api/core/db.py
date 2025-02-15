from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, StaticPool


"""
For production purposes
"""

engine = create_engine(url="sqlite:///db.sqlite3", echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Add dependency to get session
def get_session():
    with Session() as sess:
        try:
            yield sess
        finally:
            sess.close()


"""
For testing purposes
"""

TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_session():
    with TestSession() as sess:
        try:
            yield sess
        finally:
            sess.close()
