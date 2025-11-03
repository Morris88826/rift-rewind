# services/match_service.py (continued)
import time
from datetime import datetime

from flask import current_app
from extensions import db
from models.schema import Player, Match, Participant
from services.riot_api import get_match_ids_since, get_match_detail

OVERLAP_SEC = 60  # small overlap to be safe


def _get_or_create_player_by_puuid(puuid, game_name=None, tag_line=None):
    p = Player.query.filter_by(puuid=puuid).first()
    if p:
        # Fill names if we learn them later
        updated = False
        if game_name and not p.game_name:
            p.game_name, updated = game_name, True
        if tag_line and not p.tag_line:
            p.tag_line, updated = tag_line, True
        if updated:
            db.session.add(p)
        return p
    p = Player(puuid=puuid, game_name=game_name, tag_line=tag_line)
    db.session.add(p)
    return p

def _insert_match_and_participants(match_json):
    meta = match_json["metadata"]
    info = match_json["info"]
    match_id = meta["matchId"]

    # Skip if already have this match
    if Match.query.filter_by(match_id=match_id).first():
        return info.get("gameStartTimestamp", 0) // 1000

    # Create match
    m = Match(
        match_id=match_id,
        queue_id=info["queueId"],
        timestamp=datetime.fromtimestamp(info["gameStartTimestamp"] // 1000),  # convert to datetime
    )
    db.session.add(m)

    # Participants
    for p in info["participants"]:
        # Ensure Player row exists
        _get_or_create_player_by_puuid(
            p["puuid"],
            p.get("riotIdGameName") or None,
            p.get("riotIdTagline") or None,
        )

        # Insert participant row
        db.session.add(Participant(
            match_id=match_id,
            player_id=p["puuid"],              # if your model uses puuid directly
            team_id=p["teamId"],
            champion_name=p["championName"],
            win=p["win"],
            role=p["role"],
            kills=p["kills"],
            deaths=p["deaths"],
            assists=p["assists"],
            gold_earned=p["goldEarned"],
            damage_dealt=p["totalDamageDealtToChampions"],
        ))

    return info.get("gameStartTimestamp", 0) // 1000

def update_player_matches(puuid, current_year=2025, region="americas"):
    # Load the player
    player = Player.query.filter_by(puuid=puuid).first()
    if not player:
        raise ValueError("Player not found")

    if player.last_updated is None:
        last_updated_ts = 0
    else:
        try:
            last_updated_ts = int(player.last_updated.timestamp())
        except Exception as e:
            last_updated_ts = 0

    start_time = max(last_updated_ts - OVERLAP_SEC, int(datetime(current_year, 1, 1).timestamp()))
    end_time = int(datetime.now().timestamp())

    print("Updating matches for player", puuid, ", last_updated:", player.last_updated, "start_time:", datetime.fromtimestamp(start_time))
    
    num_matches = 0
    for match_id in get_match_ids_since(puuid, start_time, end_time, region=region, batch=100):
        match_json = get_match_detail(match_id, region=region)
        _insert_match_and_participants(match_json)
        num_matches += 1
        if num_matches % 10 == 0:
            db.session.commit()
            print(f"Committed {num_matches} matches so far...")

    player.last_updated = datetime.fromtimestamp(end_time)
    db.session.add(player)
    db.session.commit()

    return {
        "puuid": puuid,
        "from": start_time,
        "to": end_time,
        "processed_until": player.last_updated,
        "processed_count": num_matches
    }