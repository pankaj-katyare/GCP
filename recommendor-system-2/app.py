
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import urllib.request
import pickle
from bs4 import BeautifulSoup
import json
import sys
import lxml
from collections import OrderedDict 
import itertools

df = pd.read_csv("movie_dataset.csv")
features = ['keywords','cast','genres','director']
def combine_features(row):
    return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]
def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]

def recommendation(apikey,myTitle):
    for feature in features:
        df[feature] = df[feature].fillna('')
    df["combined_features"] = df.apply(combine_features,axis=1)
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)

    movie_user_likes = myTitle
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies =  list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
    i=0
    rec_movies=[]
    rec_posters=[]
    rec_titles=[]
    for element in sorted_similar_movies:
        #print(get_title_from_index(element[0]))
        rec_title=get_title_from_index(element[0])
        rec_titles.append(get_title_from_index(element[0]))
        #search_movie(apiKey,movie)
        response=search_movie(apikey,rec_title)
        json_str = json.dumps(response)
        resp = json.loads(json_str)
        try:
            rec_posters.append(resp['Poster'])
        except:
            rec_posters.append('static/default.png')
        i=i+1
        if i>=6:
            break
    rec_movies = {rec_titles[i]: rec_posters[i] for i in range(len(rec_titles))}
    return rec_movies

def search_movie(apiKey,movie):
    data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
    year = ''
    #movie = 'Fast & Furious' 
    params = {
        't':movie,
        'type':'movie',
        'y':year,
        'plot':'full'
    }
    response = requests.get(data_URL,params=params).json()
    return response

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/rec_list', methods=['POST','GET'])
def rec_list():
    users = ['Ryan']
    genre = ['Action', 'Science', 'Comedy', 'Fiction', 'Drama', 'Thriller']
    genre_rating=[]
    if request.method == 'POST':
        mov1 = int(request.form["mov1"])
        genre_rating.append(mov1)
        mov2 = int(request.form["mov2"])
        genre_rating.append(mov2)
        mov3 = int(request.form["mov3"])
        genre_rating.append(mov3)
        mov4 = int(request.form["mov4"])
        genre_rating.append(mov4)
        mov5 = int(request.form["mov5"])
        genre_rating.append(mov5)
        mov6 = int(request.form["mov6"])
        genre_rating.append(mov6)
    

    temp_movies=[]
    rec_movies=[]
    temp_movies = {genre[i]: genre_rating[i] for i in range(len(genre))}
    #temp_movies={key: [key, value] for key, value in zip(genre,genre_rating)}
    rec_movies=dict(reversed(sorted(temp_movies.items(), key=lambda item: item[1])))
    rec_movies= dict(itertools.islice(rec_movies.items(), 2))  
    print(rec_movies)
    return render_template('rec_list.html',movies=rec_movies)

@app.route('/search', methods=['POST','GET'])
def search1():
    return render_template('search.html')
def search2():
    return render_template('recommend.html')

@app.route('/recommend', methods=['POST','GET'])
def recommend():
    myTitle=request.form['myTitle']
    data = {}
    imdb_id="tt1190634"
    apikey='fdbe5b4'
    #data=url_for("http://www.omdbapi.com/?apikey=["+apikey+"]&?t="+myTitle)
    imdb_id="tt1190634"
    response=search_movie(apikey,myTitle)
    json_str = json.dumps(response)

    #load the json to a string
    resp = json.loads(json_str)

    #print the resp
    print (resp)
    try:
        imdb_id=resp['imdbID']
        poster=resp['Poster']
        year=resp['Year']
        rated=resp['Rated']
        released=resp['Released']
        runtime=resp['Runtime']
        plot=resp['Plot']
        poster=resp['Poster']
        r = requests.get(url="https://www.imdb.com/title/"+imdb_id+"/")
    except:
        return render_template('search.html')

    #extract an element in the response
    #print (resp['title'])

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

    #recommending movies
    rec_movies=[] 
    rec_movies=recommendation(apikey,myTitle)

    return render_template('recommend.html',year=year,released=released,runtime=runtime,plot=plot,poster=poster,myTitle=myTitle, rec_movies= rec_movies,title=title, ratingValue= ratingValue, ratingCount= ratingCount, titleName= data["name"],reviews=reviews_list)


if __name__ == "__main__":
    app.run(debug=True)
