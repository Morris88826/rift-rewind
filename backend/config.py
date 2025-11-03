import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///riot.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")