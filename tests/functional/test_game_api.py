import json

from .. import log


def test_show_all_matches_in_game(client):
    list = client.get("/api/game/1/match")
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 404


def test_create_match_in_game(client):
    new_game = client.post(
        "api/game/1/match",
        json={
            "round_number": 0,
            "player1_id": 1,
            "player2_id": 2,
            "match_date": "2024-01-01",
        },
    )
    json_data = new_game.get_json()
    log.info(json_data)
    assert new_game.status_code == 201


def test_create_second_failed_match_in_game(client):
    new_game = client.post(
        "api/game/1/match",
        json={
            "round_number": 0,
            "player1_id": 1,
            "player2_id": 2,
            "match_date": "2024-01-01",
        },
    )
    json_data = new_game.get_json()
    log.info(json_data)
    assert new_game.status_code == 201


def test_get_match_status(client):
    status = client.get("api/game/1/match/1")
    json_data = status.get_json()
    log.info(json_data)
    assert status.status_code == 200


def test_show_all_matches_in_game_should_be_one_game(client):
    list = client.get("/api/game/1/match")
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 200
    assert len(json_data["data"]) == 1


def test_add_event_to_match(client):
    game_id = 1
    match_id = 1
    json_data1 = {
        "event_type": "BALL_POTTED",
        "data": {"ball_number": 1, "pocket_id": 1},
        "write": "True",
    }
    json_data2 = {
        "event_type": "BALL_POTTED",
        "data": {"ball_number": 6, "pocket_id": 5},
        "write": "True",
    }
    json_data3 = {
        "event_type": "BALL_POTTED",
        "data": {"ball_number": 2, "pocket_id": 4},
        "write": "True",
    }

    response1 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data1),
        content_type="application/json",
    )
    response2 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data2),
        content_type="application/json",
    )
    response3 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data3),
        content_type="application/json",
    )
    response_json1 = response1.get_json()
    response_json2 = response2.get_json()
    response_json3 = response3.get_json()

    log.debug(response_json1)
    log.debug(response_json2)
    log.debug(response_json3)
    assert response_json1["data"]["event"] is not None


def test_show_all_events_in_match(client):
    list = client.get("/api/game/1/match/1/events")
    json_data = list.get_json()
    log.info(json_data)
    assert list.status_code == 200
    assert len(json_data["data"]) == 2


def test_full_game_scenario(client):
    game_id = 1
    match_id = 1

    # Удар по шару, шар попадает в лузу
    json_data1 = {
        "event_type": "HIT_BALL",
        "data": {"ball_number": 1, "pocket_id": 1},
        "write": "True",
    }
    response1 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data1),
        content_type="application/json",
    )
    response_json1 = response1.get_json()
    log.debug(response_json1)
    assert response1.status_code == 200
    assert response_json1["data"]["description"] == "Игрок забил шар 1 в лузу 1"

    # Пустой удар, переход хода
    json_data2 = {
        "event_type": "HIT_BALL",
        "data": {"ball_number": None, "pocket_id": None},
        "write": "True",
    }
    response2 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data2),
        content_type="application/json",
    )
    response_json2 = response2.get_json()
    log.debug(response_json2)
    assert response2.status_code == 200
    assert response_json2["data"]["description"] == "Переход хода: пустой удар"

    # Удар по шару противника, переход хода
    json_data3 = {
        "event_type": "HIT_BALL",
        "data": {"ball_number": 8, "pocket_id": 3},
        "write": "True",
    }
    response3 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data3),
        content_type="application/json",
    )
    response_json3 = response3.get_json()
    log.debug(response_json3)
    assert response3.status_code == 200
    assert (
        response_json3["data"]["description"] == "Переход хода: удар по шару противника"
    )

    # Выпадение шара со стола, переход хода
    json_data4 = {
        "event_type": "HIT_BALL",
        "data": {"ball_number": 4, "pocket_id": "off_table"},
        "write": "True",
    }
    response4 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data4),
        content_type="application/json",
    )
    response_json4 = response4.get_json()
    log.debug(response_json4)
    assert response4.status_code == 200
    assert response_json4["data"]["description"] == "Переход хода: шар 4 выпал со стола"

    # Выигрышный удар
    json_data5 = {
        "event_type": "HIT_BALL",
        "data": {"ball_number": 8, "pocket_id": 2},
        "write": "True",
    }
    response5 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data5),
        content_type="application/json",
    )
    response_json5 = response5.get_json()
    log.debug(response_json5)
    assert response5.status_code == 200
    assert response_json5["data"]["description"] == "Игра завершена: Игрок победил"

    json_data6 = {
        "event_type": "HIT_BALL",
        "data": {"ball_number": 8, "pocket_id": 1},
        "write": "True",
    }
    response6 = client.post(
        f"/api/game/{game_id}/match/{match_id}/event",
        data=json.dumps(json_data6),
        content_type="application/json",
    )
    response_json6 = response6.get_json()
    log.debug(response_json6)
    assert response6.status_code == 200
    assert response_json6["data"]["description"] == "Игра завершена: Игрок проиграл"
