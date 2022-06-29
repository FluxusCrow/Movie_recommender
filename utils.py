'''
use to read in data and store utility functions
'''

import pandas as pd
from thefuzz import process

movies = pd.read_csv('data/movies.csv', index_col=0) # read in data here
ratings = ...

# from Ilona
def id_to_title(movies_df, id):
    '''
    transforms moveId to title
    '''
    title = movies_df.query(f'movieId =={id}')['title'].values[0]
    return title

# from max
def title_to_id(movies_df, title):
    '''
    transforms title to movieId
    '''
    title_to_id = movies_df[movies_df['title']==title].index[0]
    return title_to_id

# from Ilona with teamwork
def fuzzy_title_to_id(movies_df, title_from_user):
    '''
    input user movie title
    returns movie title, fuzz score and movieId
    '''
    title_full = process.extract(f'{title_from_user}', movies_df['title'], limit=1)
    return title_full

def cos_sim(vec1, vec2):
    """function to calcualte the cosine similarity between two vectors""" 
    num = np.dot(vec1, vec2)
    denom = np.sqrt(np.dot(vec1, vec1)) * np.sqrt(np.dot(vec2, vec2))
    return num / denom



if __name__ == '__main__':

    print(id_to_title(movies_df=movies, id=148))
    print(title_to_id(movies, 'Toy Story (1995)'))

    












    '''
    def match_title(query, movies_df, n_results=3):
        matches = process.extract(query, movies_df['title'], limit=n_results)
        title_ids = [(match[0], match[2]) for match in matches]
        return title_ids
    '''
    
    