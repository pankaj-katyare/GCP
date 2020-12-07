

import numpy as np
import tensorflow as tf
print(tf.__version__)

users = ['Ryan']
movies = ['Star Wars', 'The Dark Knight', 'Shrek', 'The Incredibles', 'Bleu', 'Memento']
features = ['Action', 'Sci-Fi', 'Comedy', 'Cartoon', 'Drama']

num_users = len(users)
num_movies = len(movies)
num_feats = len(features)
num_recommendations = 2

users_movies = tf.constant([
                [2,  5, 0 ,  0, 8, 0]],dtype=tf.float32)

movies_feats = tf.constant([
                [1, 1, 0, 0, 1],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [1, 0, 1, 1, 0],
                [0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1]],dtype=tf.float32)

users_feats = tf.matmul(users_movies,movies_feats)
#users_feats

users_feats = users_feats/tf.reduce_sum(users_feats,axis=1,keepdims=True)
#users_feats

top_users_features = tf.nn.top_k(users_feats, num_feats)[1]
#top_users_features

for i in range(num_users):
    feature_names = [features[int(index)] for index in top_users_features[i]]
    print('{}: {}'.format(users[i],feature_names))

#We will use the dot product as our similarity measure. In essence, this is a weighted movie average for each user.

users_ratings = tf.matmul(users_feats,tf.transpose(movies_feats))
#users_ratings

#If a user has already rated a movie, we ignore that rating. This way, we only focus on ratings for previously unseen/unrated movies.

users_ratings_new = tf.where(tf.equal(users_movies, tf.zeros_like(users_movies)),
                                  users_ratings,
                                  tf.zeros_like(tf.cast(users_movies, tf.float32)))
#users_ratings_new

top_movies = tf.nn.top_k(users_ratings_new, num_recommendations)[1]
#top_movies

rec_movies=[]
for i in range(num_users):
    movie_names = [movies[index] for index in top_movies[i]]
    print('{}: {}'.format(users[i],movie_names))
    print(top_movies[i])
    rec_movies.append(movie_names)
print(rec_movies)
for movie1 in rec_movies:
    for movie2 in movie1:
        print(movie2)




