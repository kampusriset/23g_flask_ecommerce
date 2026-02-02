from flask import Flask, render_template, request, redirect, url_for, session, flash
from data import get_new_arrivals, get_top_selling, get_styles, get_brands, get_product_by_id
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import config

import matplotlib.pyplot as plt
from controllers import user_controller, admin_controller, halamanutama_controller
app = Flask(__name__)
app.config.from_object(config)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Default Route

@app.route('/')
def home():
    # Public home page (no login required)
    new_arrivals = get_new_arrivals()
    top_selling = get_top_selling()
    styles = get_styles()
    brand = get_brands()
    return render_template(
        'home.html',
        new_arrivals=new_arrivals,
        top_selling=top_selling,
        styles=styles,
        brand=brand,
        username=session.get('username')
    )

# Tempat Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    return user_controller.login(mysql, bcrypt)

# Tempat Registrasi

@app.route('/register', methods=['GET', 'POST'])
def register():
    return user_controller.register(mysql, bcrypt)

@app.route('/home')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Load data Setelah login check
    new_arrivals = get_new_arrivals()
    top_selling = get_top_selling()
    styles = get_styles()
    brand = get_brands()

    return render_template(
        'home.html',
        new_arrivals=new_arrivals,
        top_selling=top_selling,
        styles=styles,
        brand=brand,
        username=session['username']
    )

@app.route('/newarrivals')
def newarrivals():
    return halamanutama_controller.newarrivals()

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    return halamanutama_controller.productdetails(product_id)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    return halamanutama_controller.add_to_cart()

@app.route('/cart')
def cart():
    return halamanutama_controller.cart()

@app.route('/cart/update', methods=['POST'])
def update_cart():
    return halamanutama_controller.update_cart()

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return halamanutama_controller.checkout(mysql)


@app.route('/history')
def history():
    return halamanutama_controller.history(mysql)

# Profile Settings
@app.route('/account/settings', methods=['GET', 'POST'])
def account_settings():
    return user_controller.account_settings(mysql, bcrypt)

# Logout
@app.route('/logout')
def logout():
    return user_controller.logout()

                #                                      TEMPAT ADMIN                                #

    #Login Halaman Admin
@app.route('/admin')
def admin():
    return admin_controller.admin(mysql)

@app.route('/admin/merk', methods=['GET', 'POST'])
def merk_list():
    return admin_controller.merk_list(mysql)

@app.route('/admin/merk/<int:merk_id>/delete', methods=['POST'])
def merk_delete(merk_id):
    return admin_controller.merk_delete(mysql,merk_id)

@app.route('/admin/merk/export/csv')
def export_merk_csv():
    return admin_controller.export_merk_csv(mysql)

@app.route('/admin/orders', methods=['GET', 'POST'])
def order_list():
    return admin_controller.order_list(mysql)

@app.route('/admin/products', methods=['GET', 'POST'])
def product_list():
    return admin_controller.product_list(mysql)

@app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
def product_delete(product_id):
    return admin_controller.product_delete(mysql, product_id)

@app.route('/admin/customers')
def customer_list():
    return admin_controller.customer_list(mysql)
    
if __name__ == "__main__":
    app.run(debug=True)

