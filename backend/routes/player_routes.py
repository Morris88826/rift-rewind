
from services.match_service import update_player_matches
from flask import Blueprint, request, jsonify
from services import player_service
from services.riot_api import get_puuid

player_bp = Blueprint("players", __name__)

@player_bp.route("", methods=["GET"])
def get_all_players():
    players = player_service.list_players()
    return jsonify([player.to_dict() for player in players])

# Example route: get a player by puuid
@player_bp.route("/<puuid>", methods=["GET"])
def get_player(puuid):
    player = player_service.get_player_by_puuid(puuid)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(player.to_dict())

@player_bp.route("/puuid", methods=["POST"])
def fetch_puuid():
    data = request.json
    game_name = data.get("game_name")
    tag_line = data.get("tag_line")
    region = data.get("region")
    if not game_name or not tag_line or not region:
        return jsonify({"error": "Both game_name and tag_line are required"}), 400
    try:
        puuid = get_puuid(game_name, tag_line, region)
        if not puuid:
            return jsonify({"error": "Failed to fetch PUUID"}), 400
        return jsonify({"puuid": puuid})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

# Example route: create a new player
@player_bp.route("", methods=["POST"])
def create_player():
    data = request.json
    new_player = player_service.create_player(data)
    if not new_player:
        return jsonify({"error": "Failed to create player"}), 400
    return jsonify(new_player.to_dict()), 201


@player_bp.route("/<puuid>/sync", methods=["POST"])
def sync_player(puuid):
    out = update_player_matches(puuid, current_year=2025)
    return jsonify(out)
