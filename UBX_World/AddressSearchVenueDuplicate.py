import pandas as pd
import re
from itertools import combinations
from pathlib import Path


# Function to sanitize venue names (handles NaN values)
def sanitize_venue_name(street_address):
    if pd.isna(street_address):  # Check if the value is NaN
        return ''
    return re.sub(r'\s+', '', street_address.lower())


# Function to compute similarity score
def similarity_score(street_address1, street_address2):
    street_address1, street_address2 = sanitize_venue_name(street_address1), sanitize_venue_name(street_address2)
    total_chars = max(len(street_address1), len(street_address2))
    common_chars = sum(1 for a, b in zip(street_address1, street_address2) if a == b)
    return common_chars / total_chars if total_chars > 0 else 0


# Load the dataset from a CSV file
data_in_path = Path(__file__).parent / 'data-in'
data_out_path = Path(__file__).parent / 'data-out'
file_path = data_in_path / 'venues_separated.csv'
df = pd.read_csv(file_path)

# Step 1: Sanitize venue names
df['SanitizedStreetAddress'] = df['StreetAddress'].apply(sanitize_venue_name)

# Step 2: Set similarity threshold
similarity_threshold = 0.8

# Step 3: Compare each pair of venue names
groups = []
for (i, StreetAddress1), (j, StreetAddress2) in combinations(df[['Id', 'StreetAddress']].itertuples(index=False), 2):
    score = similarity_score(StreetAddress1, StreetAddress2)
    if score >= similarity_threshold:
        groups.append((i, j, StreetAddress1, StreetAddress2, score))

# Step 4: Create a DataFrame with the groups
group_df = pd.DataFrame(groups, columns=['Venue1_Id', 'Venue2_Id', 'Venue_StreetAddress1', 'Venue_StreetAddress2', 'Similarity'])

# Step 5: Save results to a new CSV file or display them
group_df.to_csv(data_out_path / 'similar_venues_Street_Address.csv', index=False)
print(group_df.head())  # Show top similar venues
