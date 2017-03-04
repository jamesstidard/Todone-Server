import pytest

from todone import create_app


@pytest.fixture
def app():
    return create_app()
