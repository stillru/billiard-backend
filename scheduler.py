from flask import Flask

from utils import log
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from extensions import db
from models.season import Season
from models.game import Game


def get_current_season_dates():
    now = datetime.now()
    year = now.year

    if now.month in [3, 4, 5]:  # Весна
        start_date = datetime(year, 3, 1)
        end_date = datetime(year, 5, 31)
        season_name = f"Spring {year}"
    elif now.month in [6, 7, 8]:  # Лето
        start_date = datetime(year, 6, 1)
        end_date = datetime(year, 8, 31)
        season_name = f"Summer {year}"
    elif now.month in [9, 10, 11]:  # Осень
        start_date = datetime(year, 9, 1)
        end_date = datetime(year, 11, 30)
        season_name = f"Autumn {year}"
    else:  # Зима
        start_date = datetime(year, 12, 1)
        end_date = (
            datetime(year + 1, 2, 28) if year % 4 != 0 else datetime(year + 1, 2, 29)
        )
        season_name = f"Winter {year}-{year + 1}"

    log.info(f"{season_name} started from {start_date} till {end_date} is selected.")
    return season_name, start_date, end_date


def check_season(app: Flask):
    log.info("Start job 'check_season'...")

    # Обернем код в контекст приложения
    with app.app_context():
        current_season = Season.query.filter_by(is_active=True).first()
        today = datetime.now().date()

        if not current_season or today > current_season.end_date:
            # Закрыть текущий сезон, если он существует
            if current_season:
                current_season.is_active = False
                db.session.commit()

                season_name, start_date, end_date = get_current_season_dates()

                # Переместить незаконченные игры в новый сезон
                unfinished_games = Game.query.filter_by(
                    season_id=current_season.id, is_finished=False
                ).all()
                new_season = Season(
                    start_date=start_date, end_date=end_date, name=season_name
                )
                db.session.add(new_season)
                db.session.commit()

                for game in unfinished_games:
                    game.season_id = new_season.id
                    db.session.commit()

            else:
                # Создать новый сезон, если ни один не существует
                season_name, start_date, end_date = get_current_season_dates()
                new_season = Season(
                    start_date=start_date, end_date=end_date, name=season_name
                )
                db.session.add(new_season)
                db.session.commit()
                log.info(f"New season - {season_name} - started!")
        else:
            log.info(f"Current season is active! {current_season.to_dict()}")


def start_scheduler(app: Flask):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_season, "cron", hour=0, minute=0, second=1, args=[app]
    )  # Запускаем задачу раз в день
    with app.app_context():
        scheduler.start()
        log.info("Scheduler started and job 'check_season' is scheduled.")
