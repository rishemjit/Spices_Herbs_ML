from collections import Counter
from numpy import array, eye, hstack, ones, vstack, zeros
import cvxopt
from cvxopt.glpk import ilp
import time
from itertools import chain

# OPTIMIZATION Approach 

def Min_cover_set(dict_data, top_set,bot_set, adjmtx, c):
    # bot_set: indications   top_set: spice set
    import time
    start = time. time()
    n1 = adjmtx.shape[0]
    n2 = adjmtx.shape[1]
    a = ones((1,n1))[0]
    x_min = 0
    x_max = 1
    #c = hstack([ones(n2), [0]])
    G1 = zeros((n1,n2 + 1))
    G1[0:n1, 0:n2] = -adjmtx
    G1[:, n2] = -zeros(n1)
    h1 = -a
    x_min = x_min * ones(n2)
    x_max = x_max * ones(n2)

    G2 = vstack([
            hstack([+eye(n2), zeros((n2, 1))]),
            hstack([-eye(n2), zeros((n2, 1))])])
    h2 = hstack([x_max, -x_min])

    c = cvxopt.matrix(c)

    G = cvxopt.matrix(vstack([G1, G2]))
    h = cvxopt.matrix(hstack([h1, h2]))

    (status, sol) = ilp(c,   # c parameter
                        G,     # G parameter
                        h,     # h parameter
                        I=set(range(0, len(c))))
    print('status', status)
    end = time. time()
    count = 0
    
    # confirm all indications are covered:
    indications_covered = []
    min_coverset = []
    for i in range(len(sol)):
        if sol[i] > 0 :
            count += 1
            min_coverset.append(list(top_set)[i])
            indications_covered.extend(dict_data[list(top_set)[i]])
            sh = list(top_set)[i]
    indications_coverset = set(indications_covered)
    print('All indications are covered: ', len(indications_coverset) == len(bot_set))
    return min_coverset


# GREEDY Approach

# input: dict_data, dict_data_reverse,
# dict_data: {spice/herb: indication list}; dict_data_reverse: {indication: spice/herb list}
    
def Min_cover_set_greedy(dict_data, dict_data_reverse):
    freq_dict_spiceherb = {}
    for s in dict_data.keys():
        freq_dict_spiceherb.update({s: len(dict_data[s])})
    # indication nodes list in order (sorted from node with least spice/herb connection to one with most)
    Bi_indic_sorted = sorted(dict_data_reverse, key = lambda k : len(dict_data_reverse[k]), reverse = False) 
    indic_visited = []
    min_cover = [] # list of spice/herb that could cover all indications
    for indic in Bi_indic_sorted:
        if indic not in indic_visited:
            sub_freq_dict = {s: freq_dict_spiceherb[s] for s in dict_data_reverse[indic]}
            
            # for each spice/herb, update the freq as (original freq - num_overlap with indic_visited)
            for s in sub_freq_dict.keys():
                num_overlap = len(list(set(indic_visited).intersection(set(dict_data[s]))))
                sub_freq_dict[s] = sub_freq_dict[s] - num_overlap

            sub_freq_sorted = sorted(sub_freq_dict.items(), key = lambda p: p[1], reverse= True)  # sorted by value(freq) from high to low
            
            # if the spice/herb with highest freq already in min_cover, skip this indication 
            # if the highest freq spice/herb already in min_cover, means this indication already be visited, so could exclude above step       
            min_cover.append(sub_freq_sorted[0][0])
            indic_visited.extend(dict_data[sub_freq_sorted[0][0]])
            indic_visited = list(set(indic_visited))
    return min_cover