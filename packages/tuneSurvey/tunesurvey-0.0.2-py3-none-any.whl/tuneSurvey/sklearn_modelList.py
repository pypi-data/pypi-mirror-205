from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import BaggingRegressor, AdaBoostRegressor, GradientBoostingRegressor

from sklearn.linear_model import LinearRegression, ElasticNet

from sklearn.cross_decomposition import PLSRegression
from sklearn.tree import DecisionTreeRegressor
#from pyearth import Earth

from m5py import M5Prime, export_text_m5
from cubist import Cubist



modelList_sklearn_regressor = [{'modelInit' : ElasticNet(),
             'par':{'alpha': [.1,.5,1.0],
                   'l1_ratio': np.linspace(0.0,1.0,11),
                   'max_iter' : [1000000]}},
             {'modelInit':PLSRegression(),
             'par':{'n_components': [1,2,3,4,5]}},#n<= min samples features targets
             {'modelInit' : SVR(),
              'par' : { 'C':[10000,1000, 100, 10, 1, .1],
                     'epsilon': [0.1, 0.01, 0.05, 0.001],
                     'gamma': ['scale', 'auto']}},
             {'modelInit' : DecisionTreeRegressor(),
             'par':{'ccp_alpha': [0.0, 0.01,0.02,0.03],
                    'criterion': ['squared_error','friedman_mse'],'max_depth': [5,10,None]}},
             {'modelInit' : BaggingRegressor(),
             'par' : {'n_estimators': [5,10,15]}},
             {'modelInit' : RandomForestRegressor(),
              'par' : {'n_estimators': [10, 50, 100, 150, 200, 400, 600]}},
             {'modelInit' : AdaBoostRegressor(),
              'par' : {'learning_rate': [.1, 1]}},
             {'modelInit' : GradientBoostingRegressor(),
              'par' : {'learning_rate': [.1, 1]}},
             {'modelInit' : Cubist(),
             'par':{'n_rules':[400,500,600],
                   'unbiased' : [True, False]}}
            ]

modelList_sklearn_classifier = [{'modelInit' : SVC(),
              'par' : { 'C':[10, 1, .1]}},
             {'modelInit' : DecisionTreeClassifier(),
             'par':{'ccp_alpha': [0.0, 0.01,0.02,0.03],
                    'criterion': ['log_loss', 'entropy', 'gini'],'max_depth': [5,10]}},
             {'modelInit' : BaggingClassifier(),
             'par' : {'n_estimators': [5,10,15]}},
             {'modelInit' : RandomForestClassifier(),
              'par' : {'n_estimators': [10, 50, 100, 150, 200, 400]}},
             {'modelInit' : AdaBoostClassifier(),
              'par' : {'learning_rate': [.1, 1]}},
             {'modelInit' : GradientBoostingClassifier(),
              'par' : {'learning_rate': [.1, 1]}}
            ]

def search_s(modelList, search_function, cv=5):
	"""cv can take in integer or cv object like tscv()
	"""
	gdresult_s = []
	for m in modelList:
		gdresult_s.append(search_function(m["modelInit"], param_grid = m["par"], cv=cv).fit(X,y))
	return gdresult_s


def get_models_sklearn(gdresult_s):
	return list(map(lambda x: x.best_estimator_,gdresult_s))

def get_predictors_sklearn(gdmodel_s):
	return list(map(lambda x: x.predict,gdmodel_s))

def get_best_scores_sklearn(gdmodel_s):
	return list(map(lambda x: x.best_score_, gdresult_s))

