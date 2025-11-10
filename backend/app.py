import os
import logging
from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
from models import schema
from routes.player_routes import player_bp
from routes.chat_routes import chat_bp
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Application factory."""
    app = Flask(__name__)

    # Load config based on environment
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    if config_name == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object(Config)

    logger.info(f"Creating app with config: {config_name}")

    # Enable CORS - configure for production
    if config_name == "production":
        CORS(app, resources={
            r"/api/*": {
                "origins": os.getenv("ALLOWED_ORIGINS", "https://yourdomain.com").split(","),
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type"],
            }
        })
    else:
        # Development: allow all origins
        CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(player_bp, url_prefix="/api/v1/players")
    app.register_blueprint(chat_bp, url_prefix="/api/v1/chat")

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {error}")
        return {"error": "Internal server error"}, 500

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    # Use environment variables for host/port
    host = os.getenv("FLASK_HOST", "localhost")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"

    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
