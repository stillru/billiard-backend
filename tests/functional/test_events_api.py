from .. import log


def test_event_create_game(client):
    player1 = client.post(
        "/api/register",
        json={
            "name": "John Doe",
            "email": "test7@example.com",
            "password": "password123",
            "new_player": True,
        },
    )
    player2 = client.post(
        "/api/register",
        json={
            "name": "Cony McCalahan",
            "email": "test8@example.com",
            "password": "password123",
            "new_player": True,
        },
    )
    data_player1 = player1.get_json()
    data_player2 = player2.get_json()
    response = client.post(
        "/api/event",
        json={
            "event_type": "start_game",
            "player1_id": data_player1["data"]["id"],
            "player2_id": data_player2["data"]["id"],
        },
    )
    assert response.status_code == 201


def test_add_second_game(client):
    response = client.post(
        "/api/event",
        json={
            "event_type": "start_game",
            "player1_id": 1,
            "player2_id": 2,
        },
    )
    json_data = response.get_json()
    log.info(json_data)
    assert response.status_code == 201


def test_show_events(client):
    list = client.get("/api/event")
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 200
