import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/hybrid_auth.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False