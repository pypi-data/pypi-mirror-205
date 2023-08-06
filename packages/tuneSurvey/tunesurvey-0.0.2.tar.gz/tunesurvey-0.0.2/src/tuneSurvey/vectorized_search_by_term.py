def vectorized_Search_hyperparameter(model, parameters, X, Y,cv =  5,search_function = GridSearchCV,verbose =False):
    """
    # model - type of model (SVR(), randomForest()...)
    # X - predictor - all rows of X are used for prediction, but each model only gives on entry in Y
    # Y - matrix containing n_var number of column vectors as target of the prediction
    # cv - cross validation type (scikit-learn obj) passed in to model selection type.
    # cv is either a number for k fold or a model selection obj for esample, cv = TimeSeriesSplit(n_splits=2, max_train_size=None, test_size=2, gap=0)
    """
    modelName = model.__class__.__name__
    
    #Series with verbose for debugging
    n_obs, n_var = Y.shape
    m_Yi = []# Collecting the model for each term in the row of the time series
    for i in range(n_var):
        if verbose:
            print("working on:" + str(modelName),"model",i)
        m_Yi.append(search_function(model, param_grid = parameters, cv=cv).fit(X,Y[:,i]))
    return m_Yi


def saveModelList_s(modelList,X,Y,path="sklModels",verbose=verbose):
    """save a list of model named by modelSequence() convention"""
    pgd = ParameterGrid(modelList['par'])
    if verbose:
        print("Permutating models and saving")
    for i, pars in enumerate(pgd):
        m = deepcopy(modelList['modelInit'])
        if verbose:
            print(pars)
            print(m)
        m = m(**pars)
        m.fit(X,Y)
        filename = ""
        for k,val in pars.items():
            filename += k+str(val).replace(".","-")
            
        dump(m,os.path.join(path,filename+".joblib"))
        gc.collect()


def modelSequence(par):
    """get names of saved files in a modelList"""
    pgd = ParameterGrid(par)
    s = []
    

    
    for i, pars in enumerate(pgd):
        
        filename = ""
        for k,val in pars.items():
            filename += k+str(val).replace(".","-")
        s.append(filename)
    return s


# X exterior train
# Y exterior test

def vectorize_model(X,Y,mtd):
    """
    #m - fitted model
    #mtd - method to create the model, e.x. SVM(parameters....).fit(data...)
    """
    n_var = Y.shape[2]
    modelList = []
    for i in range(n_var):
        m = mtd(X,Y[i])
        modelList.append(X,Y[i],m)
    return modelList

def rolling_1_day_vectorize_model(X,Y,predmtd):
    
    Y_t = np.empty_like(Y)
    
    nr, nc = Y.shape
    for i in range(nr):
        for j in range(nc):
            mj = deepcopy(predmtd[j])
            Y_t[i,j] = mj(X)
        X = Y_t[i,:]
    return Y_t
    
def sample_1_day_vectorize_model(X,Y,predmtd):
    Y_t = np.empty_like(Y)
    
    nr, nc = Y.shape
    for i in range(nr):
        for j in range(nc):
            mj = deepcopy(predmtd[j])
            Y_t[i,j] = mj(X)
        X = Y[i,:]
    return Y_t

def time_category_aggregate(df, timeIdentifier, spaceGroupIdentifier, timeStep=1, i_include=1, need_sort = True):
    """turn dataframe with time, space-group observation rows into rows with unique time id
    (sequential), count by each space-group with an interval containing i_include terms, with increment timeStep.
    complexity is close to sorting.(need_sort=True).
    If pre-sorted w.r.t. time is done, then need only approx O(n) time for n=number of rows in the origional df.
    """

    max_time_diff = max(df[timeIdentifier])


    #df = df.dropna(how='any')
    df = df.sort_values([timeIdentifier])
    spaceVec = list(set(list(df[spaceGroupIdentifier])))

    c_along_spaceVec = range(len(spaceVec)) # unique location identifier
    space_map_c = list(map(lambda x: spaceVec.index(x),df[spaceGroupIdentifier])) #this can be even faster by int(PDQ)
    timeVec = list(set(list(df[timeIdentifier])))
    l = len(df)
    ts_aggregate = []
    t1=time()

    i=0

    while i+i_include<l:
        space_aggregate = np.zeros(len(spaceVec),int)
        for j in range(i,i+i_include):
            space_aggregate[space_map_c[j]]+=1 #can also be faster eliminating i_include>timestep
        ts_aggregate.append(space_aggregate)
        i+=timeStep

    pd.DataFrame(ts_aggregate,columns = spaceVec)



def ts_feature_flatten(df,n):
    """flatten time series df (each row is one time unit), flatten all features prev n days to a row"""
    order_features = n
    n_obs,n_var = df.shape
    X = np.zeros([n_obs-order_features+1, order_features*n_var])
    #yjs are the columns
    for i in range(n_obs - order_features+1):
        for j in range(order_features):
            for k in range(n_var):
                X[i,k+j*n_var] = df[i+j,k]
    return X




def append_rolling_vectorize_model(train,test,predmtd,n=1,verbose =False):
    """ one fit rolling prediction
    predmtd is a list of function each taking in all features to predict one term in y.
    n - order that prediction model requires
     train ORIGIONAL ts df
    """
    Y_t = np.empty_like(test)
    
    nr, nc = Y_t.shape
    
    rolling_df  = train[-n:,:]
    X = ts_feature_flatten(rolling_df,n=n)
    if verbose:
        print(X)
    
    for i in range(nr):
        for j in range(nc):
            mj = predmtd[j]
            Y_t[i,j] = mj(X)
        rolling_df = np.concatenate((rolling_df[-n+1:,:],Y_t[[i],:]))
        if verbose:
            print(rolling_df)
        X = ts_feature_flatten(rolling_df,n=n)
    return Y_t

def append_rolling_vectorize_model_with_sample(train,test,predmtd,n=1):
    """ one fit rolling prediction
    n - order that prediction model requires
    train ORIGIONAL ts df
    """
    Y_t = np.empty_like(test)
    
    nr, nc = Y_t.shape
    
    rolling_df  = train[-n:,:]
    X = ts_feature_flatten(rolling_df,n=n)
    
    
    for i in range(nr):
        for j in range(nc):
            
            mj =predmtd[j]
            Y_t[i,j] = mj(X)
        rolling_df = np.concatenate((rolling_df[-n+1:,:],test[[i],:]))
        X = ts_feature_flatten(rolling_df,n=n)
    return Y_t


def reduce_best_rolling_predictor_s(predictorList, Y_train, Y_test, criterion,n, verbose = False):
    """find which row is the best predictor"""
    nModels = len(predictorList)
    nVars = len(predictorList[0])
    current_best_score = float('-inf')
    for i in range(nModels):
        predictorVec = predictorList[i]
        score_1 = criterion(Y_train,Y_test, predictorVec,n)
        if score_1>current_best_score:
            
            current_best_score = score_1
            best_model_index = deepcopy(i)
            if verbose:
                print("current best model index  ", best_model_index, "score ", score_1)
    return best_model_index


def reduce_best_rolling_predictor(predictorList, Y_train, Y_test, criterion,n, verbose = False):
    """Find which combination (one model for each term) gives the best model, combine into a row of predictors
    used in append_rolling_vectorized_modell_with_sample()"""
    nModels = len(predictorList)
    nVars = len(predictorList[0])
    current_best_score = float('-inf')
    for i in itertools.product(*list(itertools.repeat(list(range(nModels)),nVars))):
        predictorVec = []
        col=0
        
        for j in i:
            predictorVec.append(predictorList[j][col])
            col += 1
        score_1 = criterion(Y_train,Y_test, predictorVec,n)
        if score_1>current_best_score:
            current_best_score = score_1
            best_model_index = deepcopy(i)
            if verbose:
                print("current best model index  ", best_model_index)
    return best_model_index
