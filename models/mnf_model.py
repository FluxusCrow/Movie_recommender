from tkinter.ttk import Separator
import numpy as np 
from sklearn.decomposition import NMF
import pandas as pd
import seaborn as sns
import pickle

ratings_filled = pd.read_csv("../data/ratings_filled.csv", index_col=0, header=0, low_memory=False)
print(ratings_filled)
movieIds = [Id for Id in ratings_filled.columns]

nmf = NMF(n_components=200, max_iter=500)
nmf.fit(ratings_filled)

Q = pd.DataFrame(nmf.components_, columns=movieIds)

P = pd.DataFrame(nmf.transform(ratings_filled), index=ratings_filled.index)

ratings_rec = pd.DataFrame(np.dot(P, Q), index=ratings_filled.index, columns=movieIds)
#print(abs(ratings_filled-ratings_rec))
#print(nmf.reconstruction_err_)

binary = pickle.dumps(nmf)
open("nmf_model.bin", "wb").write(binary)
binary_Q = pickle.dumps(Q)
open("Q.bin", "wb").write(binary_Q)
