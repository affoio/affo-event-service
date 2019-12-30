import pytest


@pytest.fixture(scope="session")
def client(app, db):
    return app.test_client()
