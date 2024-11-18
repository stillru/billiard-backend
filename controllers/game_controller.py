from flask_smorest import abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Match, Game
from models.match import MatchStatus
from schemas.match import MatchSchema
from utils import log


class MatchService:
    match_schema = MatchSchema()
    matches_schema = MatchSchema(many=True)

    def start_match(self, game_id):
        log.info(f"{__name__} - start creating 'match'")
        match_game = Match.query.filter(Match.game_id == game_id).first()

        if not match_game:
            log.debug("No active match found.")
            game = Game.query.filter(Game.id == game_id).first()
            return self._create_match(game_id, game)

        if self._is_active_match(game_id):
            log.debug("Active match found.")
            return self.match_schema.dump(self._is_active_match(game_id)), {
                "warning": "Active match exists!"
            }

        next_id = self._get_next_match_id(game_id)
        self._create_match(game_id, next_id)
        return next_id

    def get_match_status(self, game_id, match_id):
        match_status = self._retrieve_match_status(game_id, match_id)
        if not match_status:
            raise ValueError("Match not found.")
        return match_status

    def update_match_status(self, game_id, match_id, data):
        match_status = self._retrieve_match_status(game_id, match_id)
        if not match_status:
            raise ValueError("Match not found.")

        self._apply_move(match_status, data)
        result = self._check_match_result(match_status)
        return result

    def _is_active_match(self, game_id):
        return Match.query.filter(
            Match.status == MatchStatus.IN_PROGRESS, Match.game_id == game_id
        ).first()

    def _get_next_match_id(self, game_id):
        latest_match = (
            db.session.query(Match)
            .filter(Match.game_id == game_id)
            .order_by(Match.id.desc())
            .first()
        )
        return (latest_match.id + 1) if latest_match else 1

    def _create_match(self, game_id, match_id=None, game=None):
        if game is None:
            game = Game.query.filter(Game.id == game_id).first()
        new_match = Match(
            game_id=game_id, player1_id=game.player1_id, player2_id=game.player2_id
        )

        try:
            log.debug(f"Creating new match: {new_match}")
            db.session.add(new_match)
            db.session.commit()
            log.debug(f"Match created: {new_match}")
            return self.match_schema.dump(new_match)
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

    def _retrieve_match_status(self, game_id, match_id):
        log.debug(f"Retrieving status for match {match_id} in game {game_id}")
        match = Match.query.filter(
            Match.id == match_id, Match.game_id == game_id
        ).first()
        return self.match_schema.dump(match)

    def _apply_move(self, match_status, data):
        # Implement the logic to apply a move to the match
        pass

    def _check_match_result(self, match_status):
        # Implement the logic to check the result of the match
        pass
