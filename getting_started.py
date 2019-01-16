from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import als, item_knn as knn
from lenskit.metrics import topn as tnmetrics

import pandas as pd
import matplotlib.pyplot as plt
ratings = pd.read_csv('ml-100k/u.data', sep='\t',
                      names=['user', 'item', 'rating', 'timestamp'])
print(ratings.head())

algo_ii = knn.ItemItem(20)
algo_als = als.BiasedMF(50)

def eval(aname, algo, train, test):
    fittable = util.clone(algo)
    algo.fit(train)
    users = test.user.unique()
    # the recommend function can merge rating values
    recs = batch.recommend(algo, users, 100,
            topn.UnratedCandidates(train), test)
    # add the algorithm
    recs['Algorithm'] = aname
    return recs

all_recs = []
test_data = []
for train, test in xf.partition_users(ratings[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)):
    test_data.append(test)
    all_recs.append(eval('ItemItem', algo_ii, train, test))
    all_recs.append(eval('ALS', algo_als, train, test))

all_recs = pd.concat(all_recs, ignore_index=True)
print(all_recs.head())

test_data = pd.concat(test_data, ignore_index=True)

user_dcg = all_recs.groupby(['Algorithm', 'user']).rating.apply(tnmetrics.dcg)
user_dcg = user_dcg.reset_index(name='DCG')
print(user_dcg.head())

ideal_dcg = tnmetrics.compute_ideal_dcgs(test)
print(ideal_dcg.head())

user_ndcg = pd.merge(user_dcg, ideal_dcg)
user_ndcg['nDCG'] = user_ndcg.DCG / user_ndcg.ideal_dcg
print(user_ndcg.head())

print(user_ndcg.groupby('Algorithm').nDCG.mean())
user_ndcg.groupby('Algorithm').nDCG.mean().plot.bar()
plt.show()

