from flask import render_template, request, redirect, url_for, session, flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
def login(mysql, bcrypt):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password, admin FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[2], password):
            session['username'] = user[1]
            session['admin'] = user[3]
            
            if user[3] == 1:  # Check if admin
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')

class RegisterForm(FlaskForm):
     username = StringField("Username", validators=[DataRequired()])
     password = PasswordField("Password", validators=[DataRequired()])
     submit = SubmitField("Register")

def register(mysql, bcrypt):
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        existing = cur.fetchone()
  

        if existing:
            flash("Username already exists")
            cur.close()
            return redirect(url_for('register'))

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        mysql.connection.commit()
        cur.close()

        flash("Account created successfully!")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

def account_settings(mysql, bcrypt):
    if 'username' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, first_name, last_name, email, phone, address FROM users WHERE username = %s", (session['username'],))
    user_data = cur.fetchone()
    cur.close()

    user = {
        'id': user_data[0],
        'username': user_data[1],
        'password': user_data[2],
        'first_name': user_data[3],
        'last_name': user_data[4],
        'email': user_data[5],
        'phone': user_data[6],
        'address': user_data[7]
    }

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password:
            if new_password == confirm_password:
                hashed = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET password = %s WHERE username = %s", (hashed, session['username']))
                mysql.connection.commit()
                cur.close()
            else:
                flash("Passwords do not match")
                return redirect(url_for('account_settings'))

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s, phone = %s, address = %s WHERE username = %s",
                    (first_name, last_name, email, phone, address, session['username']))
        mysql.connection.commit()
        cur.close()

        flash("Profile updated successfully")
        return redirect(url_for('account_settings'))

    return render_template('akun.html', user=user)

def logout():
    session.pop('username', None)
    flash('Anda telah logout', 'info')
    return redirect(url_for('login'))