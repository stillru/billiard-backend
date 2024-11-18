import logging

from flask import jsonify


class EventService:
    def __init__(self, json_data, client):
        self.json_data = json_data
        self.client = client

    def handle_start_game(self):
        response = self.client.post(
            "/api/game",
            json={
                "player1_id": self.json_data.get("player1_id"),
                "player2_id": self.json_data.get("player2_id"),
            },
        )
        resp = response.get_json()
        logging.debug(resp)
        resp["event_type"] = "start_game"
        return resp

    def handle_start_play(self):
        response = self.client.post(
            f"/api/game/{self.json_data.get('game_id')}/match",
        )
        resp = response.get_json()
        resp["event_type"] = "start_play"
        return resp

    def handle_player_scored(self):
        response = self.client.post(
            f"/api/match/{self.json_data.get('game_id')}/match/{self.json_data.get('play_id')}",
            json={
                "player_id": self.json_data.get("player_id"),
                "event_type": self.json_data.get("event_eventtype"),
                "ball_number": self.json_data.get("ball_number"),
            },
        )
        return response

    def handle_end_party(self):
        response = self.client.get(f"/winreasons/{self.json_data.get('win_reason_id')}")
        if response.status_code != 200:
            return jsonify({"error": "Invalid win reason"}), 400
        win_reason = response.get_json()

        response = self.client.put(
            f"/parties/{self.json_data.get('party_id')}/end",
            json={
                "winner_id": self.json_data.get("winner_id"),
                "win_reason_id": self.json_data.get("win_reason_id"),
            },
        )
        return response
