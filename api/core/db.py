"""Database module"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, StaticPool

# Production engine and session
engine = create_engine(url="sqlite:///db.sqlite3", echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Production session generator function"""

    with Session() as sess:
        try:
            yield sess
        finally:
            sess.close()


# Unit test engine and session
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_session():
    """Unit test session generator function"""

    with TestSession() as sess:
        try:
            yield sess
        finally:
            sess.close()
