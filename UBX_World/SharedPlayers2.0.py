from typing import Set, Any, Type

import pandas as pd
import ast
from pathlib import Path
from collections import defaultdict

data_in_path = Path(__file__).parent / 'data-in'
data_out_path = Path(__file__).parent / 'data-out'
file_path = data_in_path / 'tournaments_separated.csv'
tournament_df = pd.read_csv(file_path)

# Building the inverted index of player IDs to tournaments
player_tournament_map = defaultdict(set)

#creating the map for tournaments
for _, row in tournament_df.iterrows():
    tournament_name = row['Name']
    try:
        # Convert PlayerIds string to set of integers
        player_ids_str = row['PlayerIds']
        player_ids = ast.literal_eval(player_ids_str)
        player_ids = set(map(int, player_ids))

        # Map each player ID to the tournament
        for player_id in player_ids:
            player_tournament_map[player_id].add(tournament_name)

    except Exception as e:
        print(f"Error processing tournament '{tournament_name}': {e}")

#finding shared players and generating connections
tournament_connections = defaultdict(set)  # Store tournament pairs with shared players

for player_id, tournaments in player_tournament_map.items():
    tournaments = list(tournaments)
    # Generate all combinations of tournament pairs (O(n choose 2))
    for i in range(len(tournaments)):
        for j in range(i + 1, len(tournaments)):
            tournament1, tournament2 = tournaments[i], tournaments[j]
            # Ensure the pair is stored in sorted order to avoid duplicates
            sorted_pair = tuple(sorted([tournament1, tournament2]))
            # Add the shared player to the connection
            tournament_connections[sorted_pair].add(player_id)
#output
output_data = []
for (tournament1, tournament2), shared_players in tournament_connections.items():
    output_data.append({
        "Tournament1": tournament1,
        "Tournament2": tournament2,
        "SharedPlayers": ','.join(map(str, shared_players))
    })


#output
output_df = pd.DataFrame(output_data)

# Save the output to a CSV file in the data_out_path
output_df.to_csv(data_out_path / 'SharedPlayers2.csv', index=False)

# Print the first few rows of the original DataFrame
print(tournament_df.head())