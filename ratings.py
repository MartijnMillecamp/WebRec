import pandas as pd

# read in the movielens 100k ratings with pandas
# https://grouplens.org/datasets/movielens/100k/
ratings = pd.read_csv('ml-100k/u.data', sep='\t',
        names=['user', 'item', 'rating', 'timestamp'])

def getRating(user, item):
    df = ratings
    row = df.loc[(df['user'] == user) & (df['item'] == item)]
    rating = row.iloc[0]['rating']
    return int(rating)

getRating(196,242)