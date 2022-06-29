import numpy as np 
import pandas as pd

# get data
ratings = pd.read_csv("../data/ratings.csv")

# Create pivot table from ratings
df = ratings.copy()
df.drop("timestamp", axis=1, inplace=True)
df = df.pivot(index="userId", columns="movieId", values="rating")

# fill NaNs with mean of each movie
for movie in df.columns:
    df[movie].fillna(round(df[movie].mean(), 1), inplace=True)

#df.drop("rating", axis=1, level=0, inplace=True)
print(df.columns)

# save new filled ratings table
df.to_csv("../data/ratings_filled.csv")