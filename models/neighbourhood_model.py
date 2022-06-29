#from utils import cos_sim
import pandas as pd

ratings_filled_zero = pd.read_csv("../data/ratings_filled_zeros.csv", index_col=0, header=0, low_memory=False)
print(ratings_filled_zero)

def cos_sim(vec1, vec2):
    """function to calcualte the cosine similarity between two vectors""" 
    num = np.dot(vec1, vec2)
    denom = np.sqrt(np.dot(vec1, vec1)) * np.sqrt(np.dot(vec2, vec2))
    return num / denom

df = ratings_filled_zero.copy()
df = df.T
#user_input = 