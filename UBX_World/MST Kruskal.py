import pandas as pd
import networkx as nx
from pathlib import Path


data_out_path = Path(__file__).parent / 'data-out'
file_path = data_out_path / 'SharedPlayers2.csv'

#loading data
df = pd.read_csv(file_path)

#Initiate graph
tournament_graph = nx.Graph()

#adding edges to graph
#weight = num of shared players
for _, row in df.iterrows():
    tournament1 = row['Tournament1']
    tournament2 = row['Tournament2']

    shared_players = row['SharedPlayers'].split(',')
    weight = len(shared_players)

    tournament_graph.add_edge(tournament1, tournament2, weight=weight)

#Finding MST
#Using NetworkX for assistance to find minimum spanning tree
#Inverting the weights then applying MaxST function
mst = nx.maximum_spanning_tree(tournament_graph)

#Printing MST
print("\nMaximum Spanning Tree:")
for edge in mst.edges(data=True):
    print(f"{edge[0]} -- {edge[1]} (Shared Players: {edge[2]['weight']}")


output_mst_path = data_out_path / 'MaximumSpanningTree.csv'
mst_edges = [{'Tournament1': edge[0], 'Tournament2': edge[1], 'SharedPlayers': edge[2]['weight']} for edge in mst.edges(data=True)]
mst_df = pd.DataFrame(mst_edges)
mst_df.to_csv(output_mst_path, index=False)
print(f"\nMaximum Spanning Tree saved to {output_mst_path}")



