import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fooziman-secret-key-change-in-production')
    
    _raw_uri = os.getenv('URI_DATABASE', '')
    if _raw_uri:
        SQLALCHEMY_DATABASE_URI = _raw_uri.replace('postgresql://', 'postgresql+psycopg://')
        if '?' not in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///fooziman.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
