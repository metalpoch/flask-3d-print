import os
import socket

# Forzar IPv4 para entornos sin soporte IPv6 (ej: Render + Supabase)
_original_getaddrinfo = socket.getaddrinfo
def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _ipv4_getaddrinfo

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
