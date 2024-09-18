import pandas as pd
import re
from itertools import combinations
from pathlib import Path


# Function to tokenize a string (handles NaN values)
def tokenize(text):
    if pd.isna(text):  # Check if the value is NaN
        return []
    # Tokenize by converting to lowercase and splitting by non-word characters (like spaces or punctuation)
    return re.findall(r'\w+', text.lower())


# Function to compute similarity score based on token overlap
def similarity_score_tokens(token1, token2):
    set1, set2 = set(token1), set(token2)
    common_tokens = len(set1.intersection(set2))
    total_tokens = len(set1.union(set2))
    return common_tokens / total_tokens if total_tokens > 0 else 0


# Load the dataset from a CSV file
data_in_path = Path(__file__).parent / 'data-in'
data_out_path = Path(__file__).parent / 'data-out'
file_path = data_in_path / 'venues_separated.csv'
df = pd.read_csv(file_path)

# Step 1: Tokenize venue names and street addresses
df['NameTokens'] = df['Name'].apply(tokenize)
df['StreetAddressTokens'] = df['StreetAddress'].apply(tokenize)

# Step 2: Set similarity threshold
similarity_threshold = 0.8

# Step 3: Compare each pair of venue names and street addresses
groups = []
for (i, name1, addr1), (j, name2, addr2) in combinations(
        df[['Id', 'NameTokens', 'StreetAddressTokens']].itertuples(index=False), 2):
    # Combine name and street address tokens
    tokens1 = name1 + addr1
    tokens2 = name2 + addr2

    # Calculate similarity score based on tokens
    score = similarity_score_tokens(tokens1, tokens2)

    if score >= similarity_threshold:
        # Add both Venue IDs, Names, Addresses, and the similarity score to the result
        groups.append((i, j, df.loc[df['Id'] == i, 'Name'].values[0], df.loc[df['Id'] == j, 'Name'].values[0],
                       df.loc[df['Id'] == i, 'StreetAddress'].values[0],
                       df.loc[df['Id'] == j, 'StreetAddress'].values[0], score))

# Step 4: Create a DataFrame with the groups
group_df = pd.DataFrame(groups, columns=['Venue1_Id', 'Venue2_Id', 'Venue1_Name', 'Venue2_Name',
                                         'Venue1_StreetAddress', 'Venue2_StreetAddress', 'Similarity'])

# Step 5: Save results to a new CSV file or display them
group_df.to_csv(data_out_path / 'similar_venues_with_names_and_addresses.csv', index=False)
print("Similar venues saved to 'similar_venues_with_names_and_addresses.csv'")
