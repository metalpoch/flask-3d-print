from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.nombre}>'

class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(140), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen_url = db.Column(db.String(500), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PortfolioItem {self.titulo}>'
