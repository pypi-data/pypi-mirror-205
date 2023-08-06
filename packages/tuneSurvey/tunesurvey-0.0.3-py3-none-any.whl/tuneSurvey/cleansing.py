def ts_count_from_sparse(df,
                        var_time,
                        var_category,
                        time_step=1,
                        ic = 1,
                        dropna = False):
    """Transform sparse time-category data to time series data
    data -  original data frame should have each row as an observation (long form)
    | var_time | var_category | other variables |
    the function transforms it to
    | time(each row unique, incremental | cat1 | cat2 | cat3 ...
    | 1                                 | frequency of cat 1 |2 ...
    | 2                                 | frequency at time t of 1| 2 ...
    | 3
    
    where the columns are categories
    time_step: steplength of each row increament
    ic: number of time incremental units to include
    the time must be discrete and ordered
    dropna: this drop the rows if any na is find in the row.
    Complexity is about
    n*m for n-number of uniq days, m number of uniq category
    O(nlogn) for sorting, once sorted, need only go through l/time_timestep of j if ic/timestep does not increase with n.
    
    e.x.
    
    ts_count_from_sparse(data, "DAY_DIFF", "PDQ") in the 2023 Datathon code. aggregate one time for each row. 
    each entry is the count within that time frame and PDQ number of interest
    
    """
    #data['DATE'] = pd.to_datetime(data['DATE'], format = "%Y-%m-%d")
    #data['DAY_DIFF'] = (data['DATE']-data['DATE'].min()).dt.days
    max_time_diff = max(df[var_time])
    i=0

    if dropna:
        data = df.dropna(how='any')
    else:
        data=df
    data = data.sort_values([var_time])
    spaceVec = list(set(list(data[var_category])))

    c_along_spaceVec = range(len(spaceVec)) # unique location identifier
    data["space_map_c"] = list(map(lambda x: spaceVec.index(x),data[var_category])) #this can be even faster by int(PDQ)
    timeVec = list(set(list(data[var_time])))
    l = len(data)
    ts_aggregate = []

    t1=time()

    while i+ic<l:
        space_aggregate = np.zeros(len(spaceVec),int)
        for j in range(i,i+ic):
            space_aggregate[data["space_map_c"].values[j]]+=1 #can also be faster eliminating ic>timestep
        ts_aggregate.append(space_aggregate)
        i+=time_step

    ts_aggregate = pd.DataFrame(ts_aggregate,columns = spaceVec)
    return ts_aggregate


