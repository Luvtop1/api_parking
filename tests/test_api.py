from typing import cast, Dict, Any

import pytest
from flask.testing import FlaskClient
from flask import Response
from app.models import ClientParking, Parking


@pytest.mark.parametrize(
    "url",
    [
        "/clients",
        "/clients/1",
    ],
)
def test_get_methods(client: FlaskClient, url: str) -> None:
    response: Response = client.get(url)
    response_data = cast(Dict[str, Any], response.json)
    assert response.status_code == 200
    assert isinstance(response_data, (list, dict))

def test_create_client(client: FlaskClient) -> None:
    data = {
        "name": "New",
        "surname": "Client",
        "credit_card": "9876543210987654",
        "car_number": "X999XX",
    }
    response: Response = client.post("/clients", json=data)
    response_data = cast(Dict[str, Any], response.json)
    assert response.status_code == 201
    assert "id" in response_data


def test_create_parking(client: FlaskClient) -> None:
    data = {"address": "New Parking, 1", "count_places": 20}
    response = client.post("/parkings", json=data)
    assert response.status_code == 201
    assert "id" in response.json


@pytest.mark.parking
def test_enter_parking(client: FlaskClient) -> None:
    data = {"client_id": 1, "parking_id": 1}
    response = client.post("/client_parkings", json=data)
    assert response.status_code == 201
    assert "id" in response.json
    parking_response = client.get("/parkings/1")
    assert parking_response.json["count_available_places"] == 9


@pytest.mark.parking
def test_exit_parking(client: FlaskClient, db_session: Any) -> None:
    parking = Parking.query.get(1)
    parking.count_available_places = 10
    db_session.commit()

    existing = ClientParking.query.filter_by(
        client_id=1, parking_id=1, time_out=None
    ).first()
    if existing:
        db_session.delete(existing)
        db_session.commit()

    enter_data = {"client_id": 1, "parking_id": 1}
    enter_response = client.post("/client_parkings", json=enter_data)
    assert enter_response.status_code == 201

    parking_response = client.get("/parkings/1")
    assert parking_response.json["count_available_places"] == 9

    exit_response = client.delete("/client_parkings", json=enter_data)
    assert exit_response.status_code == 200

    parking_response = client.get("/parkings/1")
    assert parking_response.json["count_available_places"] == 10
