import click
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, ContactMessage, PortfolioItem
from forms import ContactForm, LoginForm, PortfolioForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Por favor inicia sesion para acceder.'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    form = ContactForm()
    try:
        portfolio_items = PortfolioItem.query.order_by(PortfolioItem.fecha.desc()).all()
    except Exception:
        portfolio_items = []
    return render_template('index.html', form=form, portfolio_items=portfolio_items)

@app.route('/contacto', methods=['POST'])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            nombre=form.nombre.data,
            email=form.email.data,
            mensaje=form.mensaje.data
        )
        db.session.add(message)
        db.session.commit()
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
        user = User.query.filter_by(username=form.username.data).first()
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
    messages = ContactMessage.query.order_by(ContactMessage.fecha.desc()).all()
    portfolio_items = PortfolioItem.query.order_by(PortfolioItem.fecha.desc()).all()
    return render_template('admin/dashboard.html', messages=messages, portfolio_items=portfolio_items)

@app.route('/admin/portfolio/nuevo', methods=['GET', 'POST'])
@login_required
def portfolio_new():
    form = PortfolioForm()
    if form.validate_on_submit():
        item = PortfolioItem(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            imagen_url=form.imagen_url.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Pieza agregada al portafolio.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/portfolio_form.html', form=form)

@app.route('/admin/portfolio/<int:item_id>/eliminar', methods=['POST'])
@login_required
def portfolio_delete(item_id):
    item = db.get_or_404(PortfolioItem, item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Pieza eliminada del portafolio.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.cli.command('init-db')
def init_db_command():
    with app.app_context():
        db.create_all()
        click.echo('Tablas creadas correctamente.')

@app.cli.command('create-admin')
@click.argument('username', default='admin')
@click.argument('password', default='fooziman2026')
def create_admin_command(username, password):
    with app.app_context():
        if not User.query.filter_by(username=username).first():
            admin = User(username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            click.echo(f'Admin "{username}" creado.')
        else:
            click.echo(f'Admin "{username}" ya existe.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
