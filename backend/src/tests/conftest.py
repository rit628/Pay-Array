import pytest
from ..orm import db
from ..server import create_app

@pytest.fixture()
def client():
    app = create_app("test", testing=True)
    app.testing = True
    with app.test_client() as test_client:
        with app.app_context():
            db.drop_all()   # Clears database for next test
            db.create_all()
            yield test_client
