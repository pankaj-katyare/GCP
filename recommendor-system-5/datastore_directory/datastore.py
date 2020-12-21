import os

project_id = os.getenv('GCLOUD_PROJECT')

from google.cloud import datastore
from flask import current_app

datastore_client = datastore.Client()

def save_credentials(name, hashpass):
    
    kind = "users"
    #name = "username"
    users_key = datastore_client.key(kind)
    users = datastore.Entity(key=users_key)
    users["username"] = name
    users["password"] = hashpass
    datastore_client.put(users)


