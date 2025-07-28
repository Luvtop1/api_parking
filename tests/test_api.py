import pytest

from app.models import ClientParking, Parking


@pytest.mark.parametrize(
    "url",
    [
        "/clients",
        "/clients/1",
    ],
)
def test_get_methods(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client):
    data = {
        "name": "New",
        "surname": "Client",
        "credit_card": "9876543210987654",
        "car_number": "X999XX",
    }
    response = client.post("/clients", json=data)
    assert response.status_code == 201
    assert "id" in response.json


def test_create_parking(client):
    data = {"address": "New Parking, 1", "count_places": 20}
    response = client.post("/parkings", json=data)
    assert response.status_code == 201
    assert "id" in response.json


@pytest.mark.parking
def test_enter_parking(client):
    # Используем существующие данные из фикстур (client_id=1, parking_id=1)
    data = {"client_id": 1, "parking_id": 1}
    response = client.post("/client_parkings", json=data)

    # Проверяем успешное создание
    assert response.status_code == 201
    assert "id" in response.json

    # Проверяем, что количество мест уменьшилось
    parking_response = client.get("/parkings/1")
    assert parking_response.json["count_available_places"] == 9  # Было 10


@pytest.mark.parking
def test_exit_parking(client, db_session):
    # Убедимся, что парковка имеет правильное количество мест
    parking = Parking.query.get(1)
    parking.count_available_places = 10  # Принудительно устанавливаем 10 мест
    db_session.commit()

    # Удаляем существующую запись о парковке, если она есть
    existing = ClientParking.query.filter_by(
        client_id=1, parking_id=1, time_out=None
    ).first()
    if existing:
        db_session.delete(existing)
        db_session.commit()

    # Создаем новую запись о парковке
    enter_data = {"client_id": 1, "parking_id": 1}
    enter_response = client.post("/client_parkings", json=enter_data)
    print("Enter response:", enter_response.json)
    assert enter_response.status_code == 201

    # Проверяем, что места уменьшились
    parking_response = client.get("/parkings/1")
    assert parking_response.json["count_available_places"] == 9

    # Выезжаем
    exit_response = client.delete("/client_parkings", json=enter_data)
    print("Exit response:", exit_response.json)
    assert exit_response.status_code == 200

    # Проверяем, что места вернулись к исходному количеству
    parking_response = client.get("/parkings/1")
    print("Parking after exit:", parking_response.json)
    assert parking_response.json["count_available_places"] == 10
