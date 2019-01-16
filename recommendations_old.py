import pandas as pd
import numpy as np
from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import item_knn as knn
from lenskit.algorithms import funksvd as funk
from lenskit.algorithms import als

# read in the movielens 100k ratings with pandas
# https://grouplens.org/datasets/movielens/100k/
ratings = pd.read_csv('ml-100k/u.data', sep='\t',
        names=['user', 'item', 'rating', 'timestamp'])

# define the algorithm we will use
# in this case: an Item-item nearest-neighbor collaborative filtering with ratings.
# https://lkpy.readthedocs.io/en/latest/knn.html?highlight=knn
algoKNN = knn.ItemItem(30)
algoFunk = funk.FunkSVD(2)
algoAls = als.BiasedMF(6)


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

fittableALS = util.clone(algoAls)
modelAls = fittableALS.fit(train)
# select a user
users = test.user.unique()

def getRecommendationsALS(user):
    model = modelAls
    algo = algoAls
    nb_recommendations = 1
    recs = batch.recommend(algo, users, 100,
                           topn.UnratedCandidates(train), test)
    recs = batch.recommend(algo, model, users,
                           nb_recommendations, topn.UnratedCandidates(train))
    return recs[recs['user'] == user]


def getRecommendations(user, algorithm):
    '''
    Return a recommendation
    :param user: id of user you want a recommendation
    :param algorithm: "Funk" or "KNN"
    :return:
    '''
    model = modelAls
    algo = algoAls

    if algorithm == "Funk":
        print("Funk")
        algo = algoFunk
        model = modelFunk

    elif algorithm == "KNN":
        print("KNN")
        algo = algoKNN
        model = modelKNN

    elif algorithm == "ALS":
        model = modelAls
        algo = algoAls

    # Generate $nb_recommendations for the givenuser
    nb_recommendations = 1
    recs = batch.recommend(algo, model, users, nb_recommendations, topn.UnratedCandidates(train))
    return recs[recs['user'] == user]


# Only for test purpose
user = np.array(users[0])
rec = getRecommendationsALS(user)
# select columns
recColumns = rec[['item', 'score']]
# select row (normally not needed)
rowSeries = recColumns.iloc[0]
item = rowSeries.values[0]
score = rowSeries.values[1]
print(item)
print(score)
print(type(item))
