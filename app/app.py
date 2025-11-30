from flask import Flask, render_template, request, redirect, url_for, session, flash
from .data import get_new_arrivals, get_top_selling, get_styles
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'
app.config['WTF_CSRF_ENABLED'] = False
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already exists")
            return redirect(url_for('register'))

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# @app.route("/dashbord")
# def dashboard():
#     if 'username' in session:
#         return render_template('dashboard.html',                       
#     username=session['username'])
#     else:
#         flash('Silakan login terlebih dahulu', 'error')
#     return redirect(url_for('login.html'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Load data AFTER login check
    new_arrivals = get_new_arrivals()
    top_selling = get_top_selling()
    styles = get_styles()

    return render_template(
        'dashboard.html',
        new_arrivals=new_arrivals,
        top_selling=top_selling,
        styles=styles,
        username=session['username']
    )

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Anda telah logout', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
