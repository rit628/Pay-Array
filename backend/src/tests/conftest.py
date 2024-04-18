import pytest
import redis
import os
from ..orm import db
from ..server import create_app

@pytest.fixture()
def client():
    app = create_app("test", testing=True)
    app.testing = True
    cache = redis.Redis(host=os.environ.get("CACHE_CONTAINER_NAME"),
                        port=os.environ.get("CACHE_CONTAINER_PORT"),
                        db=1)
    with app.test_client() as test_client:
        with app.app_context():
            db.drop_all()   # Clears database for next test
            db.create_all() # Recreates db tables for next test
            cache.flushdb() # Clears cache for next test
            yield test_client
