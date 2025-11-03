from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
from models import schema
from routes.player_routes import player_bp
from config import Config   # ✅ import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)   # ✅ load config from your Config class

    # Enable CORS for all routes
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(player_bp, url_prefix="/api/v1/players")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
