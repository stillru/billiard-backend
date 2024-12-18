import logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import upgrade
from flask_smorest import Api
from sqlalchemy.orm import scoped_session, sessionmaker
from prometheus_flask_exporter import PrometheusMetrics

from api import player_bp, news_bp, game_bp, event_bp, season_bp, tags_bp
from extensions import db, migrate
from config import ProductionConfig, Config, TestConfig
from scheduler import start_scheduler
from utils import log

metrics = PrometheusMetrics.for_app_factory()


def create_app(config_class=ProductionConfig):
    """
    Function to create the Flask application

    :param config_class: Configuration class to use
    :return: Flask application instance
    """
    app = Flask(__name__)
    log.info(f"{app.name} is starting...")
    app.config.from_object(config_class)
    log.info(f"Config '{config_class.__name__}' configured...")

    # Configure logging based on the configuration class
    config_class.configure_logging()
    log.info("Logging is configured...")

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)
    log.info("DB and Migrations initialized...")

    # Enable CORS
    CORS(app)
    log.info("CORS configured...")

    # Initialize API
    api = Api(app)
    log.info("API framework initialized...")

    # Add metrics to application
    metrics.info('app_info', 'Application info', version='0.0.1')

    # Register blueprints
    api.register_blueprint(player_bp, url_prefix="/api", name="player_api")
    api.register_blueprint(news_bp, url_prefix="/api", name="news_api")
    api.register_blueprint(game_bp, url_prefix="/api", name="game_api")
    api.register_blueprint(event_bp, url_prefix="/api", name="event_api")
    api.register_blueprint(season_bp, url_prefix="/api/", name="season_api")
    api.register_blueprint(tags_bp, url_prefix="/api/", name="tags_api")
    log.info("Routes registred...")

    with app.app_context():
        # Start the scheduler
        start_scheduler(app)
        log.info(f"Scheduler for {app.name} should be running.")
        metrics.init_app(app)

        # Apply migrations
        if config_class.TESTING:
            upgrade(directory="migrations")
        else:
            upgrade(directory="migrations")
        log.info("Database migrations applied.")

        # Log available endpoints
        for rule in app.url_map.iter_rules():
            log.info(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")

    return app


if __name__ == "__main__":
    app = create_app(TestConfig)
    app.run(debug=True, port=5030)
