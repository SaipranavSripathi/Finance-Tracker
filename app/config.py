import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:rohitdurbha@localhost"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'
