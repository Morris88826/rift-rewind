from extensions import db
from models.schema import Player
from services.riot_api import get_puuid

def get_player_by_puuid(puuid):
    """Fetch a player from the DB by puuid"""
    return Player.query.filter_by(puuid=puuid).first()

def create_player(data):
    """Insert a new player into the DB"""

    game_name = data.get("game_name")
    tag_line = data.get("tag_line")
    region = data.get("region").lower()
    puuid = data.get("puuid")
    if not puuid:
        if not game_name or not tag_line:
            raise ValueError("Either puuid or both game_name and tag_line must be provided")
        puuid = get_puuid(game_name, tag_line, region)
    
    # Check if player already exists
    existing_player = get_player_by_puuid(puuid)
    if existing_player:
        return existing_player

    player = Player(
        puuid=puuid,
        game_name=game_name,
        tag_line=tag_line
    )
    db.session.add(player)
    db.session.commit()
    return player

def list_players():
    """Return all players"""
    return Player.query.all()
