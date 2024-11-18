import logging

from flask import current_app as app, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from decorators import format_response
from extensions import db
from models.news import News, Tag
from schemas import TagSchema, NewsSchema

log = logging.getLogger()
news_bp = Blueprint("news", __name__, description="Operation on news")
tags_bp = Blueprint("tags", __name__, description="Operations on tags")


@tags_bp.route("/tags")
class Tags(MethodView):
    @tags_bp.response(200, TagSchema(many=True))
    @format_response
    def get(self):
        """List tags"""
        tags = Tag.query.all()
        tag_schema = TagSchema(many=True)
        data = tag_schema.dump(tags)
        return data

    @tags_bp.response(201, TagSchema)
    @format_response
    def post(self):
        """Create a new tag"""
        json_data = request.get_json()
        tag_schema = TagSchema()
        try:
            new_tag = Tag(**json_data)
            db.session.add(new_tag)
            db.session.commit()
        except ValidationError as err:
            abort(400, message=str(err))
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=str(e.orig))
        except Exception as e:
            db.session.rollback()
            log.error(f"Error in POST /tags: {e}")
            abort(500, message=str(e))
        return tag_schema.dump(new_tag), 201


@news_bp.route("/news")
class Newses(MethodView):
    @news_bp.response(200, NewsSchema(many=True))
    @format_response
    def get(self):
        """List news"""
        newses = News.query.all()
        news_schema = NewsSchema(many=True)
        data = news_schema.dump(newses)
        return data

    @news_bp.response(201, NewsSchema)
    @format_response
    def post(self):
        """Create a new news item"""
        json_data = request.get_json()
        news_schema = NewsSchema()
        try:
            news_data = news_schema.load(json_data)
            news_item = News(
                title=news_data["title"],
                body=news_data["body"],
                source_type=news_data["source_type"],
            )
            db.session.add(news_item)
            db.session.commit()
        except ValidationError as err:
            log.info(f"Validation error occurred: {err} on data {json_data}")
            return {"message": str(err)}, 400
        except IntegrityError as e:
            db.session.rollback()
            return {"message": str(e.orig)}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

        return news_schema.dump(news_item), 201
