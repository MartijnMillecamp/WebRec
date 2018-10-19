import pandas as pd
import numpy as np
from lenskit import batch, topn
from lenskit import crossfold as xf
from lenskit.algorithms import item_knn as knn

# read in the movielens 100k ratings with pandas
# https://grouplens.org/datasets/movielens/100k/
ratings = pd.read_csv('ml-100k/u.data', sep='\t',
        names=['user', 'item', 'rating', 'timestamp'])

# define the algorithm we will use
# in this case: an Item-item nearest-neighbor collaborative filtering with ratings.
# https://lkpy.readthedocs.io/en/latest/knn.html?highlight=knn
algo = knn.ItemItem(30)

# split the data in a test and a training set
# for each user leave one row out for test purpose
data = ratings
nb_partitions = 1
splits = xf.partition_users(data, nb_partitions, xf.SampleN(1))
for (trainSet, testSet) in splits:
    train = trainSet
    test = testSet

# train model
model = algo.train(train)
# select a user
users = test.user.unique()


def getRecommendations(user):
    """
    Generate a recommendation for the user
    :param algo: the given algorithm
    :param model: the given trained model
    :param user: the user
    :return: recommendation
    """
    # Generate $nb_recommendations for the givenuser
    nb_recommendations = 1
    recs = batch.recommend(algo, model, users, nb_recommendations, topn.UnratedCandidates(train))
    return recs[recs['user'] == user]

user = np.array(users[0])
rec = getRecommendations(user)


# select columns
recColumns = rec[['item', 'score']]
# select row (normally not needed)
rowSeries = recColumns.iloc[0]
item = rowSeries.values[0]
score = rowSeries.values[1]
print(item)
print(score)
print(type(item))