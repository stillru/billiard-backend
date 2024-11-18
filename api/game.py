from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import logging

from decorators import format_response
from extensions import db
from models import Match
from schemas import GameSchema
from schemas.match import MatchSchema
from controllers.game_controller import MatchService
from controllers.match_controller import MatchEventService

log = logging.getLogger(__name__)
game_bp = Blueprint("game_bp", __name__)


class Services:
    match_schema = MatchSchema(session=db.session)
    matches_schema = MatchSchema(session=db.session, many=True)
    controller_match = MatchService
    controller_matchevents = MatchEventService


@game_bp.route("/game")
class HandleGame(MethodView):
    @format_response
    def post(self):
        json_data = request.json
        game_schema = GameSchema(session=db.session)
        log.info(f"POST /game")
        try:
            log.info(f"Request data: {json_data}")
            new_game = game_schema.load(json_data)
            db.session.add(new_game)
            db.session.commit()
            log.info(f"Game added: {new_game}")
            return game_schema.dump(new_game), 201
        except ValidationError as err:
            log.error(f"Validation error: {err}")
            abort(400, message=f"Validation Error: {err}")
        except IntegrityError as e:
            db.session.rollback()
            log.error(f"IntegrityError: {e.orig}")
            abort(400, message=f"IntegrityError: {str(e.orig)}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            abort(500, message="An unexpected error occurred")


@game_bp.route("/game/all")
class HandleAllGame(MethodView):
    @format_response
    def get(self):
        log.info("GET /game/all")
        matches_schema = MatchSchema(session=db.session, many=True)
        all_matches = Match.query.all()
        log.debug(f"All matches: {matches_schema.dump(all_matches)}")
        return matches_schema.dump(all_matches), 200


@game_bp.route("/game/<int:game_id>/match")
class HandleAllMatch(MethodView, Services):
    @format_response
    def post(self, game_id):
        try:
            match_id = self.controller_match.start_match(
                self.controller_match(), game_id
            )
            return jsonify({"match_id": str(match_id)}), 201
        except ValueError as e:
            log.error(f"ValueError: {e}")
            return jsonify({"error": str(e)}), 400

    @format_response
    def get(self, game_id):
        log.info(f"GET /game/{game_id}/match")
        all_matches = Match.query.filter_by(game_id=game_id).all()
        log.debug(f"Matches in game {game_id}: {self.matches_schema.dump(all_matches)}")
        for i in all_matches:
            self.controller_match.get_match_status(
                Services.controller_match(), game_id=game_id, match_id=i.id
            )
        if not all_matches:
            return (
                jsonify(
                    {"count": 0, "message": f"No current matches in game {game_id}"}
                ),
                404,
            )
        return self.matches_schema.dump(all_matches), 200


@game_bp.route("/game/<int:game_id>/match/<int:match_id>")
class HandleMatch(MethodView, Services):
    @format_response
    def get(self, game_id, match_id):
        try:
            status = self.controller_match.get_match_status(
                self.controller_match(), match_id=match_id, game_id=game_id
            )
            log.info(f"Match status: {status}")
            return jsonify(status), 200
        except Exception as e:
            log.error(f"Error retrieving match status: {e}")
            abort(500, message="An unexpected error occurred")


@game_bp.route("/game/<int:game_id>/match/<int:match_id>/events")
class HandleMatchEventsView(MethodView, Services):
    @format_response
    def get(self, game_id, match_id):
        try:
            status = self.controller_match.get_match_status(
                self.controller_match(), match_id=match_id, game_id=game_id
            )
            events = self.controller_matchevents.get_match_log(
                self.controller_matchevents(), match_id=match_id
            )
            log.info(f"Match status: {status}")
            log.info(f"Log match: {events}")
            return jsonify({"gamestate": status, "gamelog": events}), 200
        except Exception as e:
            log.error(f"Error retrieving match status: {e}")
            abort(500, message="An unexpected error occurred")


@game_bp.route("/game/<int:game_id>/match/<int:match_id>/event")
class HandleMatchEventsProcess(MethodView, Services):
    @format_response
    def post(self, game_id, match_id):
        log.info(f"Received request for game_id: {game_id}, match_id: {match_id}")
        json_data = request.get_json()
        log.info(f"Request JSON data: {json_data}")

        if not json_data:
            log.error("No JSON data provided in the request")
            abort(400, message="Invalid JSON data")

        game_type = "8ball"
        try:
            event = self.controller_matchevents.process_event(
                self.controller_matchevents(),
                match_id=match_id,
                game_type=game_type,
                data=json_data.get("data"),
                event_type=json_data.get("event_type"),
                write=json_data.get("write"),
            )
            return jsonify({"event": event}), 200
        except IntegrityError as e:
            log.error(f"Error in db: {e.orig}")
            abort(500, message="An unexpected error occurred")
        except KeyError as e:
            log.error(f"Error retrieving match status: {e}")
            abort(500, message="An unexpected error occurred")
