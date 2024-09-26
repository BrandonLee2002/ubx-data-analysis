from typing import Set, Any, Type

import pandas as pd
import ast
from pathlib import Path

data_in_path = Path(__file__).parent / 'data-in'
data_out_path = Path(__file__).parent / 'data-out'
file_path = data_in_path / 'tournaments_separated.csv'
tournament_df = pd.read_csv(file_path)

#creating the map for tournaments
tournament_player_map = {}
for _, row in tournament_df.iterrows():
    tournament_name = row['Name']
    try:
        player_ids_str = row['PlayerIds']
        player_ids = ast.literal_eval(player_ids_str)
        player_ids = set(map(int, player_ids))

        tournament_player_map[tournament_name] = player_ids
    except Exception as e:
        print(f"Error processing tournament '{tournament_name}': {e}")

#finding shared players and generating connections
connections = []

for tournament1, players1 in tournament_player_map.items():
    for tournament2, players2 in tournament_player_map.items():
        if tournament1 != tournament2:
            shared_players = players1.intersection(players2)
            if shared_players:
                # Sort tournament names to avoid duplicates (e.g. A-B and B-A)
                sorted_tournaments = tuple(sorted([tournament1, tournament2]))
                # Add connection if it hasn't been added already
                if sorted_tournaments not in connections:
                    connections.append((sorted_tournaments[0], sorted_tournaments[1], shared_players))

#output
output_data = []
for tournament1, tournament2, shared_players in connections:
    output_data.append({
        "Tournament1": tournament1,
        "Tournament2": tournament2,
        "SharedPlayers": ','.join(map(str, shared_players))
    })

#output
output_df = pd.DataFrame(output_data)

# Save the output to a CSV file in the data_out_path
output_df.to_csv(data_out_path / 'SharedPlayers.csv', index=False)

# Print the first few rows of the original DataFrame
print(tournament_df.head())

