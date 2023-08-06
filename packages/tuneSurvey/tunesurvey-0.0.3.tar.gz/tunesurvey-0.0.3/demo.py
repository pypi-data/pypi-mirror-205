# Demo


# 1 static iid tabular dataset

import numpy as np

import math

n = 200 #
s = 150 # split to exterior validation set

m = 10

X = []
for i in range(n):
    
    X.append([math.sin(i) + math.cos(j) for j in range(m)])

X = np.array(X)


y = X[:,0]
X = X[:,1:]

X_train = X[:s,:]
y_train = y[:s]
X_test = X[s:,:]
y_test = y[s:]

import tuneSurvey
from tuneSurvey.skLists import *

modelList = modelList_sklearn_regressor_lite


from joblib import parallel_backend
with parallel_backend('threading', n_jobs=-1):
    gds = search_s(modelList, X, y, cv = 5)

gdm = get_models_sklearn(gds)
predictors_s = get_predictors_sklearn(gdm)
scores = get_best_scores_sklearn(gds)

print(scores)

#
from tuneSurvey.ts_torchLists import *


