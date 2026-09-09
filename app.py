from datetime import datetime
import click
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import supabase, User
from forms import ContactForm, LoginForm, PortfolioForm

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Por favor inicia sesion para acceder.'

@app.template_filter('fmtdate')
def fmtdate(value, fmt='%d/%m/%Y'):
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return value
    if isinstance(value, datetime):
        return value.strftime(fmt)
    return value

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/')
def index():
    form = ContactForm()
    try:
        resp = supabase.table('portfolio_items').select('*').order('fecha', desc=True).execute()
        portfolio_items = resp.data
    except Exception:
        portfolio_items = []
    return render_template('index.html', form=form, portfolio_items=portfolio_items)

@app.route('/contacto', methods=['POST'])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        supabase.table('contact_messages').insert({
            'nombre': form.nombre.data,
            'email': form.email.data,
            'mensaje': form.mensaje.data
        }).execute()
        flash('Mensaje enviado correctamente! Te contactaremos pronto.', 'success')
        return redirect(url_for('index'))
    flash('Error al enviar el mensaje. Por favor revisa los campos.', 'error')
    return redirect(url_for('index') + '#contacto')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Bienvenido!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Usuario o contrasena incorrectos.', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Has cerrado sesion.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    messages = supabase.table('contact_messages').select('*').order('fecha', desc=True).execute().data
    portfolio_items = supabase.table('portfolio_items').select('*').order('fecha', desc=True).execute().data
    return render_template('admin/dashboard.html', messages=messages, portfolio_items=portfolio_items)

@app.route('/admin/portfolio/nuevo', methods=['GET', 'POST'])
@login_required
def portfolio_new():
    form = PortfolioForm()
    if form.validate_on_submit():
        supabase.table('portfolio_items').insert({
            'titulo': form.titulo.data,
            'descripcion': form.descripcion.data,
            'imagen_url': form.imagen_url.data
        }).execute()
        flash('Pieza agregada al portafolio.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/portfolio_form.html', form=form)

@app.route('/admin/portfolio/<int:item_id>/eliminar', methods=['POST'])
@login_required
def portfolio_delete(item_id):
    supabase.table('portfolio_items').delete().eq('id', item_id).execute()
    flash('Pieza eliminada del portafolio.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.cli.command('create-admin')
@click.argument('username', default='admin')
@click.argument('password', default='fooziman2026')
def create_admin_command(username, password):
    if User.exists(username):
        click.echo(f'Admin "{username}" ya existe.')
    else:
        User.create(username, password)
        click.echo(f'Admin "{username}" creado.')

if __name__ == '__main__':
    app.run(debug=True)
