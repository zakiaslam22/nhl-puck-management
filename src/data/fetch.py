import requests
import json
import os
import time

# Constants
RAW_DATA_PATH = "data/raw"
SEASON = "20252026"

TEAMS = [
    'ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ',
    'DAL', 'DET', 'EDM', 'FLA', 'LAK', 'MIN', 'MTL', 'NSH',
    'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'STL', 'SJS',
    'TBL', 'TOR', 'UTA', 'VAN', 'VGK', 'WSH', 'WPG', 'SEA'
]

def get_game_ids():
    """Get all regular season game IDs for the 2025-26 season"""
    game_ids = set()
    
    for team in TEAMS:
        url = f"https://api-web.nhle.com/v1/club-schedule-season/{team}/{SEASON}"
        response = requests.get(url)
        data = response.json()
        
        for game in data.get('games', []):
            if game['gameType'] == 2:
                game_ids.add(game['id'])
        
        print(f"✓ {team} — {len(game_ids)} unique games so far")
        time.sleep(0.2)
    
    return sorted(list(game_ids))

def fetch_game(game_id):
    """Pull play-by-play data for a single game and save to data/raw/"""
    
    file_path = f"{RAW_DATA_PATH}/{game_id}.json"
    
    # Skip if already downloaded
    if os.path.exists(file_path):
        print(f"Already have game {game_id}, skipping")
        return
    
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
    response = requests.get(url)
    data = response.json()
    
    # Save to data/raw/
    with open(file_path, 'w') as f:
        json.dump(data, f)
    
    print(f"✓ Saved game {game_id}")

def fetch_all_games():
    """Fetch play-by-play data for all 1312 regular season games"""
    
    # Create data/raw folder if it doesn't exist
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    
    # Get all game IDs
    print("Getting game IDs...")
    game_ids = get_game_ids()
    print(f"Found {len(game_ids)} games")
    
    # Fetch each game
    print("Fetching games...")
    for i, game_id in enumerate(game_ids):
        fetch_game(game_id)
        time.sleep(0.5)
        
        # Progress update every 100 games
        if i % 100 == 0:
            print(f"Progress: {i}/{len(game_ids)} games")

if __name__ == "__main__":
    fetch_all_games()