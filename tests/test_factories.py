from typing import Any


def test_create_client_with_factory(db_session: Any) -> None:
    from factories import ClientFactory

    ClientFactory._meta.sqlalchemy_session = db_session
    client = ClientFactory()
    assert client.id is not None
    assert client.name is not None
    assert client.surname is not None
    assert isinstance(client.credit_card, (str, type(None)))


def test_create_parking_with_factory(db_session: Any) -> None:
    from factories import ParkingFactory

    ParkingFactory._meta.sqlalchemy_session = db_session
    parking = ParkingFactory()
    assert parking.id is not None
    assert parking.address is not None
    assert isinstance(parking.opened, bool)
    assert parking.count_places > 0
    assert parking.count_available_places == parking.count_places
