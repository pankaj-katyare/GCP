
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

def search_movie(apiKey):
    data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
    year = ''
    movie = 'Dhadak' 
    params = {
        't':movie,
        'type':'movie',
        'y':year,
        'plot':'full'
    }
    response = requests.get(data_URL,params=params).json()
    return response

apikey='fdbe5b4'
    #data=url_for("http://www.omdbapi.com/?apikey=["+apikey+"]&?t="+myTitle)
imdb_id="tt1190634"
response=search_movie(apikey)
print(response)

