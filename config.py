import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fooziman-secret-key-change-in-production')
    
    _raw_uri = os.getenv('URI_DATABASE', '')
    SQLALCHEMY_DATABASE_URI = _raw_uri.replace('postgresql://', 'postgresql+psycopg://')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
