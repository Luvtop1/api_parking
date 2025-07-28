from datetime import datetime

from flask import Blueprint, jsonify, request

from .models import Client, ClientParking, Parking, db

api = Blueprint("api", __name__)


@api.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify(
        [
            {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "credit_card": client.credit_card,
                "car_number": client.car_number,
            }
            for client in clients
        ]
    )


@api.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(
        {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "credit_card": client.credit_card,
            "car_number": client.car_number,
        }
    )


@api.route("/clients", methods=["POST"])
def create_client():
    data = request.get_json()
    client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id}), 201


@api.route("/parkings", methods=["POST"])
def create_parking():
    data = request.get_json()
    parking = Parking(
        address=data["address"],
        opened=data.get("opened", True),
        count_places=data["count_places"],
        count_available_places=data["count_places"],
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify({"id": parking.id}), 201


@api.route("/client_parkings", methods=["POST"])
def enter_parking():
    data = request.get_json()
    client_id = data.get("client_id")
    parking_id = data.get("parking_id")

    if not client_id or not parking_id:
        return jsonify({"error": "Missing client_id or parking_id"}), 400

    client = Client.query.get(client_id)
    parking = Parking.query.get(parking_id)

    if not client:
        return jsonify({"error": "Client not found"}), 404
    if not parking:
        return jsonify({"error": "Parking not found"}), 404

    if not parking.opened:
        return jsonify({"error": "Parking is closed"}), 400

    if parking.count_available_places <= 0:
        return jsonify({"error": "No available places"}), 400

    # Проверяем, не находится ли клиент уже на парковке
    existing = ClientParking.query.filter_by(
        client_id=client_id, parking_id=parking_id, time_out=None
    ).first()

    if existing:
        return jsonify({"error": "Client already on parking"}), 400

    try:
        client_parking = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=datetime.now()
        )

        parking.count_available_places -= 1
        db.session.add(client_parking)
        db.session.commit()

        return jsonify({"id": client_parking.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@api.route("/client_parkings", methods=["DELETE"])
def exit_parking():
    data = request.get_json()
    client_id = data.get("client_id")
    parking_id = data.get("parking_id")

    if not client_id or not parking_id:
        return jsonify({"error": "Missing client_id or parking_id"}), 400

    try:
        client_parking = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first()

        if not client_parking:
            return jsonify({"error": "No active parking record found"}), 404

        client = client_parking.client
        if not client.credit_card:
            return jsonify({"error": "No credit card for payment"}), 400

        parking = client_parking.parking
        client_parking.time_out = datetime.now()

        # Убедимся, что не превышаем общее количество мест
        if parking.count_available_places < parking.count_places:
            parking.count_available_places += 1

        db.session.commit()

        return jsonify({"message": "Successfully exited"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@api.route("/parkings/<int:parking_id>", methods=["GET"])
def get_parking(parking_id):
    parking = Parking.query.get_or_404(parking_id)
    return jsonify(
        {
            "id": parking.id,
            "address": parking.address,
            "opened": parking.opened,
            "count_places": parking.count_places,
            "count_available_places": parking.count_available_places,
        }
    )
