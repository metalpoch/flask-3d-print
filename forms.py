from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10, max=1000)])

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

class PortfolioForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=2, max=140)])
    descripcion = TextAreaField('Descripción')
    imagen_url = StringField('URL de Imagen')
