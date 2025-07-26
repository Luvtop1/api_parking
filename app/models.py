from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Client(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    surname = db.Column(String(50), nullable=False)
    credit_card = db.Column(String(50), nullable=True)
    car_number = db.Column(String(10), nullable=True)

    parkings: List["ClientParking"] = relationship(
        "ClientParking", backref="client", lazy=True
    )


class Parking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "parking"

    id = db.Column(Integer, primary_key=True)
    address = db.Column(String(100), nullable=False)
    opened = db.Column(Boolean)
    count_places = db.Column(Integer, nullable=False)
    count_available_places = db.Column(Integer, nullable=False)

    clients: List["ClientParking"] = relationship(
        "ClientParking", backref="parking", lazy=True
    )


class ClientParking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client_parking"

    id = db.Column(Integer, primary_key=True)
    client_id = db.Column(Integer, ForeignKey("client.id"))
    parking_id = db.Column(Integer, ForeignKey("parking.id"))
    time_in = db.Column(DateTime, nullable=True)
    time_out = db.Column(DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )
