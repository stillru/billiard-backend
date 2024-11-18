from flask import request, jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from decorators import format_response
from controllers import EventService
from models.events import GlobalEvent
from schemas.events import GlobalEventSchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db
import logging

event_bp = Blueprint("event_bp", __name__)

logger = logging.getLogger(__name__)


@event_bp.route("/event")
class Events(MethodView):
    @event_bp.response(200)
    @format_response
    def get(self):
        events = GlobalEvent.query.all()
        events_schema = GlobalEventSchema(many=True)
        return events_schema.dump(events)

    @event_bp.response(201)
    @format_response
    def post(self):
        json_data = request.json
        event_schema = GlobalEventSchema(session=db.session)
        event_type = json_data.get("event_type")
        if event_type not in [
            "start_game",
            "player_scored",
            "end_game",
            "start_play",
            "update_play",
            "end_play",
        ]:
            abort(400, message=f"{event_type} not valid")

        event_service = EventService(json_data, current_app.test_client())
        response_data = {}
        if event_type == "start_game":
            response_data = event_service.handle_start_game()
        elif event_type == "start_play":
            response_data = event_service.handle_start_play()
        elif event_type == "end_party":
            response_data = event_service.handle_end_party()
        else:
            abort(400, message="Unsupported event type")

        if isinstance(response_data, dict):
            logging.debug(response_data)
            try:
                event_new = event_schema.load(response_data)
                db.session.add(event_new)
                db.session.commit()
                logging.debug(event_schema.dump(event_new))
                return event_schema.dump(event_new), 201
            except (ValidationError, IntegrityError) as e:
                db.session.rollback()
                abort(500, message=str(e))
            except Exception as e:
                db.session.rollback()
                abort(500, message=str(e))
        else:
            abort(400, message=response_data.get_json())
