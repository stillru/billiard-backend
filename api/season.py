import logging

from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from decorators import format_response
from extensions import db
from models.season import Season
from schemas import SeasonSchema
from decorators import format_response

season_bp = Blueprint("seasons", __name__, description="Operations on seasons")


@season_bp.route("/seasons")
class Seasons(MethodView):
    @season_bp.response(200, SeasonSchema(many=True))
    @format_response
    def get(self):
        seasons = Season.quary.all()
        season_schema = SeasonSchema(many=True)
        data = season_schema.dump(seasons)
        return data

    @season_bp.arguments(SeasonSchema)
    @season_bp.response(201, SeasonSchema)
    @format_response
    def post(self, new_season):
        season_schema = SeasonSchema()
        try:
            # Пытаемся создать экземпляр модели Season на основе данных
            season = season_schema.load(new_season, session=db.session)
            db.session.add(season)
            db.session.commit()
        except ValidationError as err:
            return {"message": str(err)}, 400
        except IntegrityError as e:
            db.session.rollback()
            return {"message": str(e.orig)}, 400

        logging.log(20, season_schema.dump(season))
        return season_schema.dump(season), 201
