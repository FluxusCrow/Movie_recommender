'''
flask app for movie recommendations
'''

from flask import Flask, request, render_template 
from utils import movies, fuzzy_title_to_id, id_to_title, title_to_id # import data read in from other scripts
from recommender import recommend_neighborhood, recommend_nmf, recommend_random # import functions from other scripts


app = Flask(__name__) # instansiate the flask object

@app.route('/') # use a decorator to route the function to a URL
def landing_page():
    return render_template('landing_page.html')

@app.route('/recommendations')
def recommendations():
    model = request.args.get("model")
    print(request.args) # shows URL aruments in terminal, not needed, used for explanation
    
    user_movies = request.args.getlist('user_movies') # stores user_movies in variable
    star_ratings = []
    star_rating1 = request.args.getlist("rate_1")
    star_rating2 = request.args.getlist("rate_2")
    star_rating3 = request.args.getlist("rate_3")
    star_rating4 = request.args.getlist("rate_4")
    star_rating5 = request.args.getlist("rate_5")
    user_ratings = request.args.getlist("user_ratings")
    star_ratings = star_rating1 + star_rating2 + star_rating3 + star_rating4 + star_rating5
    zip_inputs = zip(user_movies, star_ratings)
    user_dic = dict(zip_inputs)
    
    titles_ids = [fuzzy_title_to_id(movies_df=movies, title_from_user=user_input) for user_input in user_movies]
    # take movie ids and format them for models and recommendations
    ids = [title_to_id(movies_df= movies, title=x[0]) for i in titles_ids for x in i]
    print("Here are ids", ids)
    print("dic", user_dic)
    user_dic_new = {}
    rec_ids = []
    for count, movie in enumerate(user_dic):
        a = ids[count]
        user_dic_new[a] = user_dic[movie]
    
    print("New", user_dic_new)
    print("Model", model)
    if model == "Non-negative matrix factorisation":
        rec_ids = recommend_nmf(query=user_dic_new, movies=movies, model="nmf")
    elif model == "Clustering":
        rec_ids = [1,2,3,4,5]
    elif model == "Trending":
        rec_ids = [1,2,3,4,5]
    elif model == "Neighborhood-Based Collaborative Filtering":
        rec_ids = recommend_neighborhood(query=user_dic_new, movies=movies, model="neighbor")
    elif model == "Random":
        rec_ids = recommend_random(query=user_dic_new, movies=movies)
    print(rec_ids)
    #rec_ids = recommend_random(query=user_movies, movies=movies)
    recs = [id_to_title(movies_df=movies, id=id) for id in rec_ids]
    return render_template('recommendations.html', user_inputs=user_movies, titles_ids=titles_ids, recs=recs)


if __name__=='__main__':
    app.run(debug=True) # run the app in debug mode and reboot when changes are made

    