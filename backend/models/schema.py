from extensions import db

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    puuid = db.Column(db.String, unique=True, nullable=False)
    game_name = db.Column(db.String, nullable=False)
    tag_line = db.Column(db.String, nullable=False)
    participants = db.relationship("Participant", back_populates="player")
    last_updated = db.Column(db.DateTime, default=None) # timestamp of last update

    def to_dict(self):
        return {
            "id": self.id,
            "puuid": self.puuid,
            "game_name": self.game_name,
            "tag_line": self.tag_line,
            "last_updated": self.last_updated
        }

class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String, unique=True, nullable=False)
    queue_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    participants = db.relationship("Participant", back_populates="match")

    def to_dict(self):
        return {
            "id": self.id,
            "match_id": self.match_id,
            "queue_id": self.queue_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

class Participant(db.Model):
    __tablename__ = "participants"
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    team_id = db.Column(db.Integer) # 100 or 200 (100 = blue side, 200 = red side)
    champion_name = db.Column(db.String)
    win = db.Column(db.Boolean)
    role = db.Column(db.String)
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    gold_earned = db.Column(db.Integer)
    damage_dealt = db.Column(db.Integer)
    match = db.relationship("Match", back_populates="participants") # create relationship to Match, enable participant.match 
    player = db.relationship("Player", back_populates="participants") # create relationship to Player, enable participant.player

    def to_dict(self):
        return {
            "id": self.id,
            "match_id": self.match_id,
            "player_id": self.player_id,
            "team_id": self.team_id,
            "champion_name": self.champion_name,
            "win": self.win,
            "role": self.role,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "gold_earned": self.gold_earned,
            "damage_dealt": self.damage_dealt
        }