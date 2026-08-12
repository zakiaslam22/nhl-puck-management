import json
import os
import pandas as pd

# Constants
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"

def flatten_game(data):
    """Flatten one game's JSON into a list of rows"""
    rows = []
    
    # Game level info
    game_id = data['id']
    season = data['season']
    game_date = data['gameDate']
    venue=data['venue']
    home_team = data['homeTeam']['abbrev']
    away_team = data['awayTeam']['abbrev']
    home_score_final = data['homeTeam']['score']
    away_score_final = data['awayTeam']['score']
    
    # Build player lookup from rosterSpots
    roster = {}
    for player in data.get('rosterSpots', []):
        roster[player['playerId']] = {
            'player_name': player['firstName']['default'] + ' ' + player['lastName']['default'],
            'position_code': player['positionCode'],
            'team_id': player['teamId']
        }
    
    # Flatten each event
    for play in data.get('plays', []):
        details = play.get('details', {})
        player_id = details.get('playerId')
        
        row = {
            'game_id': game_id,
            'season': season,
            'game_date': game_date,
            'home_team': home_team,
            'away_team': away_team,
            'home_score_final': home_score_final,
            'away_score_final': away_score_final,
            'event_id': play.get('eventId'),
            'event_type': play.get('typeDescKey'),
            'sort_order': play.get('sortOrder'),
            'period': play['periodDescriptor']['number'],
            'period_type': play['periodDescriptor']['periodType'],
            'time_in_period': play.get('timeInPeriod'),
            'time_remaining': play.get('timeRemaining'),
            'situation_code': play.get('situationCode'),
            'home_team_defending_side': play.get('homeTeamDefendingSide'),
            'x_coord': details.get('xCoord'),
            'y_coord': details.get('yCoord'),
            'zone_code': details.get('zoneCode'),
            'player_id': player_id,
            'event_owner_team_id': details.get('eventOwnerTeamId'),
            'hitting_player_id': details.get('hittingPlayerId'),
            'hittee_player_id': details.get('hitteePlayerId'),
            'shooting_player_id': details.get('shootingPlayerId'),
            'scoring_player_id': details.get('scoringPlayerId'),
            'away_score': details.get('awayScore'),
            'home_score': details.get('homeScore'),
        }
        
        # Join player info from roster
        if player_id and player_id in roster:
            row['player_name'] = roster[player_id]['player_name']
            row['position_code'] = roster[player_id]['position_code']
            row['player_team_id'] = roster[player_id]['team_id']
        else:
            row['player_name'] = None
            row['position_code'] = None
            row['player_team_id'] = None
            
        rows.append(row)
    
    return rows

def build_events_df():
    """Read all raw JSON files and combine into one big dataframe"""
    
    all_rows = []
    files = os.listdir(RAW_DATA_PATH)
    
    print(f"Processing {len(files)} games...")
    
    for i, filename in enumerate(files):
        if not filename.endswith('.json'):
            continue
            
        file_path = f"{RAW_DATA_PATH}/{filename}"
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        rows = flatten_game(data)
        all_rows.extend(rows)
        
        if i % 100 == 0:
            print(f"Progress: {i}/{len(files)} games")
    
    df = pd.DataFrame(all_rows)
    print(f"Total events: {len(df)}")
    return df

def save_events_df(df):
    """Save the events dataframe to data/processed/"""
    
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    file_path = f"{PROCESSED_DATA_PATH}/events.csv"
    df.to_csv(file_path, index=False)
    print(f"Saved {len(df)} events to {file_path}")

if __name__ == "__main__":
    df = build_events_df()
    save_events_df(df)