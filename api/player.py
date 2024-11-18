import logging

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError

from models.player import Player
from extensions import db

from decorators import format_response
from models.user import User
from schemas import PlayerSchema
from schemas.user import UserSchema

player_bp = Blueprint("api", __name__)


@player_bp.route("/register")
class Register(MethodView):
    @format_response
    def post(self):
        json_data = request.json
        existing_user = User.query.filter_by(email=json_data["email"]).first()
        if existing_user:
            abort(400, message="Player already exists")
        try:
            user_schema = UserSchema(session=db.session)
            data = UserSchema.load(user_schema, data=json_data)
            logging.info(f"New player validated: {data}")
        except ValidationError as e:
            abort(400, message=f"Validation error: {e.messages}")
        except Exception as e:
            abort(400, e)
        user = User(
            name=json_data["name"],
            password=json_data["password"],
            email=json_data["email"],
        )
        db.session.add(user)
        db.session.commit()
        if "new_player" in json_data:
            player = Player(user_id=user.id, score=0, played_games=0, name=user.name)
            db.session.add(player)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "Registration successful",
                        "id": user.id,
                        "new_player": "Created",
                    }
                ),
                201,
            )
        return jsonify({"message": "Registration successful", "id": user.id}), 201
