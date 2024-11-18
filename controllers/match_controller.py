import json
import os

from flask import jsonify
from flask_smorest import abort
from marshmallow import ValidationError

from extensions import db
from models import Event, EventType
from models.events import FoulEventData, BallPottedEventData, HitBallEventData
from models.match import MatchStatus, Match
from schemas.events import (
    EventSchema,
    FoulEventSchema,
    BallPottedEventSchema,
    HitBallEventSchema,
)
from utils import log


class MatchEventService:
    """
    Controller for validationg match events
    """
    HitBallEvent = HitBallEventSchema

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rules_path = os.path.join(base_dir, "../static/rules.json")
        with open(rules_path) as f:
            self.rules = json.load(f)

    def get_match_log(self, match_id):
        events = (
            Event.query.filter(Event.match_id == match_id)
            .order_by(Event.timestamp.asc())
            .all()
        )
        values = EventSchema.dump(EventSchema(), events, many=True)
        return values

    def process_event(self, game_type, event_type, data, match_id, write=None):
        log.debug(f"Processing event for {match_id} - {event_type} with {data}")
        log.debug(f"process_event - {event_type}")
        if event_type == "HIT_BALL":
            schema = HitBallEventSchema()
        elif event_type == "BALL_POTTED":
            schema = BallPottedEventSchema()
        elif event_type == "FOUL":
            schema = FoulEventSchema()
        else:
            abort(400, message=f"Unsupported event type: {event_type}")

        try:
            validated_data = schema.load(data, session=db.session)
        except ValidationError as err:
            abort(400, message=err.messages)

        events = (
            Event.query.filter(Event.match_id == match_id)
            .order_by(Event.timestamp.asc())
            .all()
        )
        if len(events) == 0:
            match_state = {
                "balls_hit": [],
                "balls_pocketed": [],
                "current_player_id": None,
                "turns": [],
                "fouls": [],
                "game_status": "ongoing",
                "winner_id": None,
                "last_pocketed_ball": None,
                "target_pocket": None,
                "description": None,
            }
            match_state = self._apply_event(
                match_id=match_id,
                match_state=match_state,
                event_type=event_type.upper(),
                data=validated_data,
                write=write,
                player_id=1,
            )
        else:
            match_state = self._reconstruct_match_state(events, game_type, match_id)
            match_state = self._apply_event(
                match_id=match_id,
                match_state=match_state,
                event_type=event_type,
                data=validated_data,
                write=write,
            )
        if self._check_win_condition(match_state, game_type):
            self._finalize_match(match_id, match_state)
        return match_state

    def validate_event(self, match_id, game_type, event_type, data):
        # Получение правил для конкретного типа игры и события
        game_rules = self.rules.get(game_type)
        if not game_rules:
            raise ValueError(f"No rules found for game type: {game_type}")

        event_rules = game_rules.get(event_type)
        if not event_rules:
            raise ValueError(
                f"No validation rules found for event type: {event_type} in game type: {game_type}"
            )
        log.debug("Event valid")

        # Применение каждого правила валидации
        for rule in event_rules["validations"]:
            field = rule["field"]
            if rule["type"] == "required":
                self._validate_required(field, data)
            elif rule["type"] == "range":
                self._validate_range(field, data, rule["min"], rule["max"])

        log.info(
            f"Event {event_type} for match {match_id} in game {game_type} passed validation."
        )

    def _validate_required(self, field, data):
        if field not in data:
            abort(400, message=f"Field '{field}' is required for this event.")

    def _validate_range(self, field, data, min_value, max_value):
        if field in data:
            value = data[field]
            if not (min_value <= value <= max_value):
                abort(
                    400,
                    message=f"Field '{field}' must be between {min_value} and {max_value}.",
                )
        else:
            abort(400, message=f"Field '{field}' is required for this event.")

    def _reconstruct_match_state(self, events, game_type,  match_id) -> object:
        log.debug("Reconstructing match...")

        match_state = {
            "balls_hit": [],
            "balls_pocketed": [],
            "current_player_id": None,
            "turns": [],
            "fouls": [],
            "game_status": "ongoing",
            "winner_id": None,
            "last_pocketed_ball": None,
            "target_pocket": None,
            "description": None,
        }

        for event in events:
            if event.event_type == EventType.HIT_BALL:
                hit_data = HitBallEventData.query.filter_by(event_id=event.id).first()
                if hit_data:
                    match_state = self._apply_event(
                        match_id=event.match_id,
                        match_state=match_state,
                        event_type=event.event_type,
                        data={
                            "ball_number": hit_data.ball_number,
                            "force": hit_data.force,
                            "description": event.description,
                        },
                        player_id=event.player_id,
                        write=False,
                        reconstructing=True,
                    )

            elif event.event_type == EventType.BALL_POTTED:
                potted_data = BallPottedEventData.query.filter_by(
                    event_id=event.id
                ).first()
                if potted_data:
                    match_state = self._apply_event(
                        match_id=event.match_id,
                        match_state=match_state,
                        event_type=event.event_type,
                        data={
                            "ball_number": potted_data.ball_number,
                            "pocket_id": potted_data.pocket_id,
                            "description": event.description,
                        },
                        player_id=event.player_id,
                        write=False,
                        reconstructing=True,
                    )

            elif event.event_type == EventType.FOUL:
                foul_data = FoulEventData.query.filter_by(event_id=event.id).first()
                if foul_data:
                    match_state = self._apply_event(
                        match_id=event.match_id,
                        match_state=match_state,
                        event_type=event.event_type,
                        data={
                            "reason": foul_data.reason,
                            "description": event.description,
                        },
                        player_id=event.player_id,
                        write=False,
                        reconstructing=True,
                    )

        log.debug(f"Reconstructed match state: {match_state}")
        return match_state

    def _apply_event(
            self,
            match_id,
            match_state,
            event_type,
            data,
            player_id=1,
            write=False,
            reconstructing=False,
    ):
        log.debug(
            f"Applying event: {event_type} for match {match_id} with data: {data}, write={write}, player={player_id}"
        )

        if not reconstructing:
            # Создание нового события
            new_event = Event(
                match_id=match_id,
                event_type=event_type,
                player_id=player_id,
            )
            try:
                db.session.add(new_event)
                db.session.flush()  # Получаем ID для нового события до его использования в связанных таблицах
            except Exception as e:
                log.error(f"Error while adding new event: {e}")
                db.session.rollback()
                abort(500, message="Internal server error while processing event.")

        description = None  # Инициализация описания

        # Обработка типов событий
        if event_type == "HIT_BALL":
            log.debug(HitBallEventSchema.dump(self.HitBallEvent(),obj=data))
            if isinstance(data, dict):
                balls_hit = data.get("ball_number", [])
                balls_pocketed = data.get("balls_pocketed", {})
                log.debug(f"==> {balls_hit}, {balls_pocketed}")
            else:
                balls_hit = getattr(data, 'ball_number', [])
                balls_pocketed = getattr(data, 'balls_pocketed', {})
                log.debug(f"===> {balls_hit}, {balls_pocketed}")


            valid_pots = []
            invalid_pots = []

            for ball_number, pocket_id in balls_pocketed.items():
                if self._is_valid_pot(match_state, ball_number, pocket_id):
                    valid_pots.append((ball_number, pocket_id))
                    match_state["balls_pocketed"].append(ball_number)
                    log.debug(f"Valid pot: Ball {ball_number} in pocket {pocket_id}")
                else:
                    invalid_pots.append((ball_number, pocket_id))
                    log.debug(f"Invalid pot: Ball {ball_number} in pocket {pocket_id}")

            match_state["balls_hit"].extend(balls_hit)

            # Формируем описание события
            description = (
                f"Игрок {player_id} ударил шары: {', '.join(map(str, balls_hit))}. "
            )
            if valid_pots:
                description += f"Шары {', '.join([str(ball) for ball, _ in valid_pots])} забиты правильно. "
            if invalid_pots:
                description += f"Шары {', '.join([str(ball) for ball, _ in invalid_pots])} забиты неправильно. "
                foul_reason = "Неправильный шар был забит"
                description += f"Фол: {foul_reason}. Переход хода."
                match_state["fouls"].append(
                    {"player_id": player_id, "reason": foul_reason}
                )
                match_state["current_player_id"] = self._get_next_player(player_id, match_id)
                match_state["foul"] = foul_reason

            match_state["valid_pots"] = valid_pots
            match_state["invalid_pots"] = invalid_pots
            match_state["next_player"] = match_state["current_player_id"]

        elif event_type == EventType.BALL_POTTED:
            ball_number = data.get("ball_number")
            pocket_id = data.get("pocket_id")

            if not reconstructing:
                potted_data = BallPottedEventData(
                    event_id=new_event.id, ball_number=ball_number, pocket_id=pocket_id
                )
                db.session.add(potted_data)

                description = (
                    f"Игрок {player_id} забил шар {ball_number} в лузу {pocket_id}"
                )

            match_state["balls_pocketed"].append(ball_number)
            match_state["last_pocketed_ball"] = ball_number
            match_state["target_pocket"] = pocket_id
            log.debug(f"Ball potted: {ball_number}, pocket: {pocket_id}")

        elif event_type == EventType.FOUL:
            reason = data.get("reason")

            if not reconstructing:
                foul_data = FoulEventData(event_id=new_event.id, reason=reason)
                db.session.add(foul_data)

            description = f"Фол: {reason}"
            match_state["fouls"].append({"player_id": player_id, "reason": reason})
            match_state["current_player_id"] = self._get_next_player(player_id, match_id)

        # Сохранение описания события
        if description:
            if not reconstructing:
                new_event.description = description
            match_state["description"] = description

        # Запись события в базу данных
        if write and not reconstructing:
            try:
                db.session.commit()
                log.debug("Event committed to DB successfully")
            except Exception as e:
                log.error(f"Error committing event to DB: {e}")
                db.session.rollback()
                abort(500, message="Internal server error while committing event.")

        log.debug(f"Updated match_state: {match_state}")
        return match_state

    def _check_win_condition(self, match_state, game_type):
        if game_type == "8ball":
            if "8" in match_state["balls_pocketed"]:
                return True
        # Добавить другие условия для других типов игр...
        return False

    def _finalize_match(self, match_id, match_state):
        # Обновление статуса матча
        match = Match.query.get(match_id)
        match.status = MatchStatus.COMPLETED
        winner = self._determine_winner(match_state)
        match.winner = winner
        self._update_player_profiles(match.player1, match.player2, winner)
        db.session.commit()

    def _determine_winner(self, match_state):
        return "player1"

    def _update_player_profiles(self, player1, player2, winner):
        # Логика обновления профилей игроков
        if winner == player1:
            player1.wins += 1
            player2.losses += 1
        else:
            player1.losses += 1
            player2.wins += 1
        db.session.commit()

    def _get_next_player(self, player_id: object, match_id: int) -> object:
        match = Match.query.filter(Match.id == match_id).first()
        log.debug(f'Getting next player: Was {player_id}')
        if player_id == match.player1_id:
            return match.player2_id
        else:
            return match.player1_id
    def _is_valid_pot(self, match_state, ball_number, pocket_id) -> bool:
        return True
