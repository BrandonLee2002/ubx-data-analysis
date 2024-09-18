import pandas as pd
import re
from itertools import combinations
from pathlib import Path


# Function to sanitize venue names (handles NaN values)
def sanitize_venue_name(name):
    if pd.isna(name):  # Check if the value is NaN
        return ''
    return re.sub(r'\s+', '', name.lower())


# Function to compute similarity score
def similarity_score(name1, name2):
    name1, name2 = sanitize_venue_name(name1), sanitize_venue_name(name2)
    total_chars = max(len(name1), len(name2))
    common_chars = sum(1 for a, b in zip(name1, name2) if a == b)
    return common_chars / total_chars if total_chars > 0 else 0


# Load the dataset from a CSV file
data_in_path = Path(__file__).parent / 'data-in'
data_out_path = Path(__file__).parent / 'data-out'
file_path = data_in_path / 'venues_separated.csv'
df = pd.read_csv(file_path)

# Step 1: Sanitize venue names
df['SanitizedName'] = df['Name'].apply(sanitize_venue_name)

# Step 2: Set similarity threshold
similarity_threshold = 0.8

# Step 3: Compare each pair of venue names
groups = []
for (i, venue_name1), (j, venue_name2) in combinations(df[['Id', 'Name']].itertuples(index=False), 2):
    score = similarity_score(venue_name1, venue_name2)
    if score >= similarity_threshold:
        groups.append((i, j, venue_name1, venue_name2, score))

# Step 4: Create a DataFrame with the groups
group_df = pd.DataFrame(groups, columns=['Venue1_Id', 'Venue2_Id', 'Venue_Name1', 'Venue_Name2', 'Similarity'])

# Step 5: Save results to a new CSV file or display them
group_df.to_csv(data_out_path / 'similar_venues.csv', index=False)
print(group_df.head())  # Show top similar venues
