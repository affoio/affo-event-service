from infi.clickhouse_orm.database import Database

import pytest

from affo_event_service.application import create_app, create_celery


@pytest.fixture(scope="session", autouse=True)
def app(request):
    settings_override = {"TESTING": True}
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session", autouse=True)
def celery(app):
    settings_override = {"CELERY_TASK_ALWAYS_EAGER": True, "CELERY_TASK_EAGER_PROPAGATES": True}

    return create_celery(app, settings_override)


@pytest.fixture(scope="session", autouse=True)
def db(app, request):
    db_ = Database(app.name, log_statements=True)

    try:
        db_.migrate("affo_event_service.migrations")
        yield db_
    finally:
        db_.drop_database()
