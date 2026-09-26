import json
from datetime import timedelta

with open('config.json') as f:
    info = json.load(f)["info"]

class Config:
    SECRET_KEY = info['secret-key']
    SQLALCHEMY_DATABASE_URI = info['local_db_url']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=int(info['days_to_remomber']))