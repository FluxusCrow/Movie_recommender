# Movie recommender

## General info
Heroku web app to recommend movies based on different algorithms

## Technologies
* Python 3.9.7
* libraries and its versions are listed in requirements.txt and can be installed with:
```
$ conda install --name <environment_name> --file requirements.txt
```

## Setup (locally)
1. Run in the terminal:
```
$ python application.py
```

2. Click on the link provided by the terminal (similar to: http://127.0.0.1:5000/)

3. A website opens locally. Insert movies that you have seen and rate them (1 star: bad, 5 stars: good)

4. (Optionally) Choose a algorithm

5. Press "submit"

## Setup (online)
Go to https://grand-movies.herokuapp.com/

## Status
* Random recommendation, NMF and Neighborhood models are running locally, but are slow
* NMF model can't be used on the web app, because it takes too long (timeout error). The other two models run also on the web app
* Choosing trending or clustering model will simply recommend default movies, since those models are not implemented
