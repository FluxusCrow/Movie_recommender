'''
different functions for making movie recommendations
'''

import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

ratings_filled = pd.read_csv("data/ratings_filled.csv", index_col=0, header=0, low_memory=False)



def recommend_random(query, movies, k=10):
    """
    Dummy recommender that recommends a list of random movies. Ignores the actual query.
    """
    print(movies.reset_index()['movieId'].sample(k).to_list())
    return movies.reset_index()['movieId'].sample(k).to_list()


def recommend_popular(query, k=10):
    """
    Filters and recommends the top k movies for any given input query. 
    Returns a list of k movie ids.
    """    
    
    return [364, 372, 43, 34, 243]

def recommend_cluster(query, k=10):
    """
    Filters and recommends the top k movies from a cluster a given input query. 
    Returns a list of k movie ids.
    """    
    
    return [364, 372, 43, 34, 243]


def recommend_nmf(query, movies, model, k=10):
    """
    Filters and recommends the top k movies for any given input query based on a trained NMF model. 
    Returns a list of k movie ids.
    """    
    binary = open("models/nmf_model.bin", "rb").read()
    nmf = pickle.loads(binary)
    binary_Q = open("models/Q.bin", "rb").read()
    Q = pickle.loads(binary_Q)
    print(nmf.reconstruction_err_)
    inp = pd.DataFrame([[fill(query, i) for i in ratings_filled]], columns=ratings_filled.columns)
    P_input = nmf.transform(inp)
    R_input = np.dot(P_input, Q)
    recommendations_nmf = pd.DataFrame(R_input, columns=ratings_filled.columns)
    return recommendations_nmf.sort_values(by=0, axis=1, ascending=False).iloc[0,0:k].index

def fill(query, i):
    """
    Loops through all movies and looks for the movie that was part of the input and adds the rating input. Rates all other movies with the mean
    """
    if int(i) in query:
        return query[int(i)]
    else:
        return round(ratings_filled[i].mean(), 1)

def fill_zero(query, i):
    """
    Loops through all movies and looks for the movie that was part of the input and adds the rating input. Rates all other movies with 0
    """
    if int(i) in query:
        return query[int(i)]
    else:
        return 0

def recommend_neighborhood(query, movies, model, k=10):
    """
    Filters and recommends the top k movies for any given input query based on a trained nearest neighbors model. 
    Returns a list of k movie ids.
    """   
    ratings_filled_zeros_T = pd.read_csv("data/ratings_filled_zeros_T.csv", index_col=0, header=0, low_memory=False)
    ratings_filled_zeros = pd.read_csv("data/ratings_filled_zeros.csv", index_col=0, header=0, low_memory=False)
    inp_ratings = np.zeros_like(ratings_filled_zeros.columns)
    movies = ratings_filled_zeros.columns
    inp = pd.DataFrame([[fill_zero(query, i) for i in ratings_filled_zeros]], columns=ratings_filled_zeros.columns)
    user_unseen = list(inp.columns[inp.iloc[0] == 0])
    df = ratings_filled_zeros_T.copy()
    inp_id = len(ratings_filled_zeros_T.columns)+1
    df[inp_id] = list(inp.iloc[0])
    cos_sim_table = pd.DataFrame(cosine_similarity(df.T), index=df.columns, columns=df.columns)
    neighbours = list(cos_sim_table[inp_id].sort_values(ascending=False).index[1:4])


    predicted_ratings_movies = []
    for movie in user_unseen:
        # we check the users who watched the movie
        people_who_have_seen_the_movie = list(ratings_filled_zeros_T.columns[ratings_filled_zeros_T.loc[int(movie)] > 0])

        num = 0
        den = 0
        for user in neighbours:
            # if this person has seen the movie
            if user in people_who_have_seen_the_movie:
            #  we want extract the ratings and similarities
                rating = ratings_filled_zeros_T.loc[int(movie),str(user)]
                similarity = cos_sim_table.loc[inp_id,user]

            # predict the rating based on the (weighted) average ratings of the neighbours
            # sum(ratings)/no.users OR 
            # sum(ratings*similarity)/sum(similarities)
                num = num + rating*similarity
                den = den + similarity
        try:
            predicted_ratings = num/den
        except:
            predicted_ratings = 0
        predicted_ratings_movies.append([predicted_ratings,movie])
    
    df_pred = pd.DataFrame(predicted_ratings_movies, columns = ["rating", "movie"])
    df_pred.set_index("movie", inplace=True)
    
    return df_pred.sort_values(by = "rating", ascending=False).iloc[0:k].index

#recommend_neighborhood({1: 5.0, 193609: 3.2}, "n")
#print(recommend_nmf({1: 5.0, 193609: 3.2}, "n", "d"))