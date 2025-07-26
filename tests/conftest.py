from typing import Any, Dict, Generator

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Client, Parking


@pytest.fixture(scope="module")
def app() -> Generator[Flask, Any, None]:
    """Application fixture with test configuration"""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()

        client1 = Client(
            name="John",
            surname="Doe",
            credit_card="4111111111111111",
            car_number="A123BC",
        )
        client2 = Client(name="Jane", surname="Smith", car_number="B456DE")
        db.session.add_all([client1, client2])

        parking1 = Parking(
            address="Main Street, 1",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        parking2 = Parking(
            address="Second Street, 2",
            opened=False,
            count_places=5,
            count_available_places=5,
        )
        db.session.add_all([parking1, parking2])

        db.session.commit()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> TestClient:
    """Фикстура тестового клиента"""
    return app.test_client()


@pytest.fixture
def db_session(app: Flask) -> Generator[SQLAlchemy.session, Any, None]:
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture
def new_client_data() -> Dict[str, str]:
    """New client data fixture"""
    return {
        "name": "New",
        "surname": "Client",
        "credit_card": "5555555555555555",
        "car_number": "X999XX",
    }


@pytest.fixture
def new_parking_data() -> Dict[str, Any]:
    """New parking data fixture"""
    return {"address": "New Parking Address", "count_places": 15, "opened": True}


def pytest_configure(config: Any) -> None:
    """Pytest configuration"""
    config.addinivalue_line("markers", "parking: mark tests for parking functionality")
