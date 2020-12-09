import numpy as np
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import urllib.request
import pickle
from bs4 import BeautifulSoup
import tensorflow as tf

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def page1():
    return render_template('page1.html')

@app.route('/page2', methods=['POST','GET'])
def page2():
    users = ['Ryan']
    movies = ['Star Wars', 'The Dark Knight', 'Shrek', 'The Incredibles', 'Bleu', 'Memento']
    features = ['Action', 'Sci-Fi', 'Comedy', 'Cartoon', 'Drama']

    if request.method == 'POST':
        mov1 = int(request.form["mov1"])
        mov2 = int(request.form["mov2"])
        mov3 = int(request.form["mov3"])
        mov4 = int(request.form["mov4"])
        mov5 = int(request.form["mov5"])
        mov6 = int(request.form["mov6"])

    num_users = len(users)
    num_movies = len(movies)
    num_feats = len(features)
    num_recommendations = 2

    users_movies = tf.constant([
                    [mov1,  mov2, mov3 ,  mov4, mov5, mov6]],dtype=tf.float32)

    movies_feats = tf.constant([
                    [1, 1, 0, 0, 1],
                    [1, 1, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [1, 0, 1, 1, 0],
                    [0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1]],dtype=tf.float32)

    users_feats = tf.matmul(users_movies,movies_feats)
    users_feats

    users_feats = users_feats/tf.reduce_sum(users_feats,axis=1,keepdims=True)
    users_feats

    top_users_features = tf.nn.top_k(users_feats, num_feats)[1]
    top_users_features

    for i in range(num_users):
        feature_names = [features[int(index)] for index in top_users_features[i]]
        print('{}: {}'.format(users[i],feature_names))

    #We will use the dot product as our similarity measure. In essence, this is a weighted movie average for each user.

    users_ratings = tf.matmul(users_feats,tf.transpose(movies_feats))
    users_ratings

    #If a user has already rated a movie, we ignore that rating. This way, we only focus on ratings for previously unseen/unrated movies.

    users_ratings_new = tf.where(tf.equal(users_movies, tf.zeros_like(users_movies)),
                                     users_ratings,
                                     tf.zeros_like(tf.cast(users_movies, tf.float32)))
    users_ratings_new

    top_movies = tf.nn.top_k(users_ratings_new, num_recommendations)[1]
    top_movies

    temp_movies=[]
    rec_movies=[]
    for i in range(num_users):
        movie_names = [movies[index] for index in top_movies[i]]
        print('{}: {}'.format(users[i],movie_names))
        temp_movies.append(movie_names)

    for movie1 in temp_movies:
        rec_movies=movie1

    return render_template('page2.html',movies=rec_movies)

@app.route('/page3', methods=['POST','GET'])
def page3():
    data = {}
    imdb_id="tt1190634"
    r = requests.get(url="https://www.imdb.com/title/"+imdb_id+"/")
    # Create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')

    #page title
    title = soup.find('title').string

    # rating
    ratingValue = soup.find("span", {"itemprop" : "ratingValue"}).string

    # no of rating given
    ratingCount = soup.find("span", {"itemprop" : "ratingCount"}).string

    # name
    titleName = soup.find("div",{'class':'titleBar'}).find("h1")
    data["name"] = titleName.contents[0].replace(u'\xa0', u'')

    
    # web scraping to get user reviews from IMDB site
    sauce = urllib.request.urlopen('https://www.imdb.com/title/'+imdb_id+'/reviews?ref_=tt_ov_rt').read()
    soup = BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})

    reviews_list = [] 
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)  

    return render_template('page3.html',title=title, ratingValue= ratingValue, ratingCount= ratingCount, titleName= data["name"],reviews=reviews_list)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080,debug=True)
