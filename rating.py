import pandas as pd
from flask import make_response, abort, jsonify

# read in the movielens 100k ratings with pandas
# https://grouplens.org/datasets/movielens/100k/
RATINGS = pd.read_csv('ml-100k/u.data', sep='\t',
        names=['user', 'item', 'rating', 'timestamp'])

def ratings_user(user_id):
    """
    This function responds to a request for /api/ratings/{user_id}
    with complete list of ratings of that person
    :param user_id:   user_id of persons whose ratings you want
    :return:        list of ratings matching user_id
    """
    df = RATINGS
    print(user_id)
    # Does the person hava a rating?
    rows = df.loc[(df['user'] == user_id)]

    if not rows.empty:
        # select colums
        rows = rows[['item', 'rating']]
        rows_dict = rows.to_dict(orient="records")
        ratings = []
        for entry in rows_dict:
            ratings.append({
                "item" : int(entry['item']),
                "rating": int(entry["rating"])
            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No ratings for user with user_id  {user_id} ".format(user_id=user_id)
        )

    return ratings

def rating_user_item(user_id, item_id):
    """
    This function responds to a request for /api/ratings/{user_id}
    with complete list of ratings of that person
    :param user_id:   user_id of persons whose ratings you want
    :return:        list of ratings matching user_id
    """
    df = RATINGS
    print(user_id)
    # Does the person hava a rating?
    rows = df.loc[(df['user'] == user_id) & (df['item'] == item_id)]

    if not rows.empty:
        # select colums
        rows = rows[['item', 'rating']]
        rows_dict = rows.to_dict(orient="records")
        ratings = []
        for entry in rows_dict:
            ratings.append({
                "item": int(entry['item']),
                "rating": int(entry["rating"])
            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No ratings for user with user_id  {user_id} ".format(user_id=user_id)
        )

    return ratings