from datetime import datetime
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore[attr-defined]
    name = db.Column(db.String(50), nullable=False)  # type: ignore[attr-defined]
    surname = db.Column(db.String(50), nullable=False)  # type: ignore[attr-defined]
    credit_card = db.Column(db.String(50), nullable=True)  # type: ignore[attr-defined]
    car_number = db.Column(db.String(10), nullable=True)  # type: ignore[attr-defined]

    parkings: List["ClientParking"] = db.relationship(  # type: ignore[attr-defined]
        "ClientParking", backref="client", lazy=True
    )

class Parking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore[attr-defined]
    address = db.Column(db.String(100), nullable=False)  # type: ignore[attr-defined]
    opened = db.Column(db.Boolean)  # type: ignore[attr-defined]
    count_places = db.Column(db.Integer, nullable=False)  # type: ignore[attr-defined]
    count_available_places = db.Column(db.Integer, nullable=False)  # type: ignore[attr-defined]

    clients: List["ClientParking"] = db.relationship(  # type: ignore[attr-defined]
        "ClientParking", backref="parking", lazy=True
    )

class ClientParking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore[attr-defined]
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))  # type: ignore[attr-defined]
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))  # type: ignore[attr-defined]
    time_in = db.Column(db.DateTime, nullable=True)  # type: ignore[attr-defined]
    time_out = db.Column(db.DateTime, nullable=True)  # type: ignore[attr-defined]

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),  # type: ignore[attr-defined]
    )