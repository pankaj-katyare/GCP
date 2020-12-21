import os

project_id = os.getenv('GCLOUD_PROJECT')

from google.cloud import datastore
from flask import current_app

datastore_client = datastore.Client()

def save_credentials(name, hashpass):
    #key = datastore.Entity(key=datastore_client.key('username'),value=datastore_client.key('password'))
    # key = datastore_client.key('credentials')
    # q_entity = datastore.Entity(key=key)
    # for q_prop, q_val in credentials.items():
    #     q_entity[q_prop] = q_val

    # datastore_client.put(q_entity)
    kind = "users"
    #name = "username"
    users_key = datastore_client.key(kind)
    users = datastore.Entity(key=users_key)
    users["username"] = name
    users["password"] = hashpass
    datastore_client.put(users)

#def get_user(name):
    # q=users.all()
    # q.filter("username=",name)
    # result = q.get()
    # return result

    #query=datastore_client.query(kind="users")
    #user_detail = list(query.fetch(username=name))
    #return user_detail

    #query=datastore_client.query(kind="users")
    #query.add_filter("username","=",name)
    # Res=query.fetch()

    #query = datastore_client.query()
    #res = list(query.fetch())

    #query=datastore_client.query(kind="users")
    #query.add_filter("username","=",name)
