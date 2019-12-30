import uuid

import pytest

from affo_event_service.models.event import Event


@pytest.mark.parametrize(
    "event_data",
    [
        {
            "cf1": None,
            "cf2": None,
            "cf3": None,
            "cf4": None,
            "cf5": None,
            "cid": "00000000000000000000000000000000",
            "cn": "Test Company",
            "dl": "http://example.com",
            "dr": None,
            "t": "pageview",
            "tid": "affo.3kTMd",
            "uip": "127.0.0.1",
            "utt": "2019-01-01 00:00:00",
            "ua": None,
        },
    ],
)
def test_api_event(client, event_data, db):
    response = client.post("/api/v1.0/event/", json=event_data)
    assert response.status_code == 200

    assert Event.objects_in(db).count() == 1

    event = Event.objects_in(db)[:1][0]

    for key in event_data:
        if key == "cid":
            assert uuid.UUID(event_data[key]) == getattr(event, key)
        elif key == "t":
            assert event_data[key] == getattr(event, key).name
        else:
            assert str(event_data[key]) == str(getattr(event, key))
