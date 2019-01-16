import pandas as pd
import numpy as np
from lenskit import batch, topn
from lenskit import crossfold as xf
from lenskit.algorithms import item_knn as knn
from lenskit.algorithms import funksvd as funk
from lenskit.algorithms import als

from flask import make_response, abort, jsonify


# read in the movielens 100k ratings with pandas
# https://grouplens.org/datasets/movielens/100k/
ratings = pd.read_csv('ml-100k/u.data', sep='\t',
        names=['user', 'item', 'rating', 'timestamp'])

algoKNN = knn.ItemItem(30)
algoFunk = funk.FunkSVD(2)
algoAls = als.BiasedMF(20)


# split the data in a test and a training set
# for each user leave one row out for test purpose
data = ratings
nb_partitions = 1
splits = xf.partition_users(data, nb_partitions, xf.SampleN(1))
for (trainSet, testSet) in splits:
    train = trainSet
    test = testSet

# train model
modelKNN = algoKNN.fit(train)
modelFunk = algoFunk.fit(train)
modelALS = algoAls.fit(train)
users = test.user.unique()



def get_recommendations_Funk_SVD(user_id, nb_recommendations = 1):
    '''
    Return a recommendation
    :param user: id of user you want a recommendation
    :param algorithm: "Funk"
    :return:
    '''
    algo = algoFunk
    model = modelFunk

    recs = batch.recommend(algo, model, users, nb_recommendations, topn.UnratedCandidates(train))
    recs = recs[recs['user'] == user_id]
    if not recs.empty:
        # select colums
        rows = recs[['item', 'score']]
        rows_dict = rows.to_dict(orient="records")
        recommendations = []
        for entry in rows_dict:
            recommendations.append({
                "item": int(entry['item']),
                "score": int(entry["score"])
            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No ratings for user with user_id  {user_id} ".format(user_id=user_id)
        )



    return recommendations

def get_recommendations_KNN(user_id, nb_recommendations = 1):
    '''
    Return a recommendation
    :param user: id of user you want a recommendation
    :param algorithm: "Funk"
    :return:
    '''
    algo = algoKNN
    model = modelKNN

    recs = batch.recommend(algo, model, users, nb_recommendations, topn.UnratedCandidates(train))
    recs = recs[recs['user'] == user_id]
    if not recs.empty:
        # select colums
        rows = recs[['item', 'score']]
        rows_dict = rows.to_dict(orient="records")
        recommendations = []
        for entry in rows_dict:
            recommendations.append({
                "item": int(entry['item']),
                "score": int(entry["score"])
            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No ratings for user with user_id  {user_id} ".format(user_id=user_id)
        )
    return recommendations

def get_recommendations_als(user_id, nb_recommendations = 1):
    '''
    Return a recommendation
    :param user: id of user you want a recommendation
    :param algorithm: "Funk"
    :return:
    '''
    algo = algoFunk
    model = modelFunk

    recs = batch.recommend(algo, model, users, nb_recommendations, topn.UnratedCandidates(train))
    recs = recs[recs['user'] == user_id]
    if not recs.empty:
        # select colums
        rows = recs[['item', 'score']]
        rows_dict = rows.to_dict(orient="records")
        recommendations = []
        for entry in rows_dict:
            recommendations.append({
                "item": int(entry['item']),
                "score": int(entry["score"])
            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No ratings for user with user_id  {user_id} ".format(user_id=user_id)
        )
    return recommendations