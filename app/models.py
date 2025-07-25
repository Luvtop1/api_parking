from datetime import datetime
from typing import List, Optional

from . import db


class Client(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    surname: str = db.Column(db.String(50), nullable=False)
    credit_card: Optional[str] = db.Column(db.String(50))
    car_number: Optional[str] = db.Column(db.String(10))

    parkings: List["ClientParking"] = db.relationship(
        "ClientParking", backref="client", lazy=True
    )


class Parking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "parking"

    id: int = db.Column(db.Integer, primary_key=True)
    address: str = db.Column(db.String(100), nullable=False)
    opened: bool = db.Column(db.Boolean)
    count_places: int = db.Column(db.Integer, nullable=False)
    count_available_places: int = db.Column(db.Integer, nullable=False)

    clients: List["ClientParking"] = db.relationship(
        "ClientParking", backref="parking", lazy=True
    )


class ClientParking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client_parking"

    id: int = db.Column(db.Integer, primary_key=True)
    client_id: int = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id: int = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in: Optional[datetime] = db.Column(db.DateTime)
    time_out: Optional[datetime] = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )
