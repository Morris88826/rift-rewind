import time
from flask import current_app
import requests
from config import Config

def get_puuid(game_name, tag_line, region="americas"):
    """Fetch the puuid for a given Riot ID (game_name#tag_line)"""
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {
        "X-Riot-Token": Config.RIOT_API_KEY
    }
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        return data.get("puuid")
    else:
        print("Error:", resp.status_code, resp.json())
    return None


def _sleep_on_429(resp, attempt):
    if resp.status_code != 429:
        return False
    retry_after = resp.headers.get("Retry-After")
    if retry_after:
        time.sleep(int(retry_after))
    else:
        time.sleep(min(2 ** attempt, 16))
    return True

def get_match_ids_since(puuid, start_time, end_time, region="americas", batch=100):
    """Yield match IDs in pages, resilient to 429 and partial failures."""
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": Config.RIOT_API_KEY}
    start = 0

    while True:
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "start": start,
            "count": batch
        }
        attempt = 0
        while True:
            resp = requests.get(url, headers=headers, params=params)
            if resp.status_code == 200:
                break
            if _sleep_on_429(resp, attempt):
                attempt += 1
                continue
            # log & stop this page on other errors
            current_app.logger.warning("match ids error %s: %s", resp.status_code, resp.text)
            return

        ids = resp.json()
        if not ids:
            return
        for mid in ids:
            yield mid
        start += batch
        time.sleep(0.1)  # gentle pacing
        

def get_match_detail(match_id, region="americas"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": current_app.config["RIOT_API_KEY"]}

    attempt = 0
    while True:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        if _sleep_on_429(resp, attempt):
            attempt += 1
            continue
        raise RuntimeError(f"Fetch match {match_id} failed {resp.status_code}: {resp.text}")