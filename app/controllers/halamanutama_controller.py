from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from data import get_product_by_id, get_new_arrivals, format_price_display
import sys

def parse_price(price):
   
    if isinstance(price, int):
        return price
    if isinstance(price, str):
        return int(price.split()[0])
    return int(price)

def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    

    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('dashboard'))

    cart = session['cart']
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'quantity': quantity
        }
    
    session.modified = True
    flash(f'{product["name"]} added to cart!', 'success')
    return redirect(url_for('cart'))

def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart_items = []
    subtotal = 0
    
    if 'cart' in session:
        for product_id, item in session['cart'].items():

            price = parse_price(item['price'])
            item_total = price * item['quantity']
            subtotal += item_total
            cart_items.append({
                'id': item['id'],
                'name': item['name'],
                'price': price,
                'price_display': format_price_display(price),
                'image': item['image'],
                'qty': item['quantity'],
                'total': item_total,
                'total_display': format_price_display(item_total)
            })
    
    delivery = 5  #Bayar Denda Karna Pajak Ongkos
    total = subtotal + delivery
    
    return render_template(
        'cart.html',
        items=cart_items,
        subtotal=subtotal,
        subtotal_display=format_price_display(subtotal),
        delivery=delivery,
        delivery_display=format_price_display(delivery),
        total=total,
        total_display=format_price_display(total),
        discount=0
    )

def update_cart():
    product_id = str(request.form.get('product_id'))
    action = request.form.get('action', 'update')
    
    if 'cart' not in session:
        return redirect(url_for('cart'))
    
    cart = session['cart']
    
    if action == 'remove':
        
        if product_id in cart:
            del cart[product_id]
            flash('Item removed from cart', 'info')
    else:
        
        quantity = int(request.form.get('quantity', 0))
        if quantity <= 0:
            
            if product_id in cart:
                del cart[product_id]
                flash('Item removed from cart', 'info')
        else:
            if product_id in cart:
                cart[product_id]['quantity'] = quantity
                flash('Cart updated', 'success')
    
    session.modified = True
    return redirect(url_for('cart'))

def checkout(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        
        try:
            cur = mysql.connection.cursor()
            
            if 'cart' in session:
                for product_id, item in session['cart'].items():
                    quantity = item['quantity']
                    price = parse_price(item['price'])
                    
                    print(f"DEBUG: Processing product_id={product_id}, quantity={quantity}, price={price}", file=sys.stderr)
                   
                    cur.execute('SELECT merk_id FROM produk WHERE produk_id = %s', (int(product_id),))
                    product_result = cur.fetchone()
                    
                    print(f"DEBUG: Query result: {product_result}", file=sys.stderr)
                    
                    if product_result:
                        merk_id = product_result[0]
                        profit = price * quantity 
                        
                        print(f"DEBUG: Updating merk_id={merk_id}, quantity={quantity}, profit={profit}", file=sys.stderr)
                        
                        cur.execute('''
                            UPDATE merk 
                            SET jumlahpenjualan = jumlahpenjualan + %s,
                                keuntungan = keuntungan + %s
                            WHERE merk_id = %s
                        ''', (quantity, profit, merk_id))
                        
                        print(f"DEBUG: Rows affected: {cur.rowcount}", file=sys.stderr)
                    else:
                        print(f"DEBUG: Product not found for product_id={product_id}", file=sys.stderr)
            
            mysql.connection.commit()
            cur.close()
            
            flash('Order placed successfully!', 'success')
            session['cart'] = {}
            session.modified = True
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            mysql.connection.rollback()
            flash(f'Error processing order: {str(e)}', 'danger')
            return redirect(url_for('cart'))
    
    cart_items = []
    subtotal = 0
    
    if 'cart' in session:
        for product_id, item in session['cart'].items():
            price = parse_price(item['price'])
            item_total = price * item['quantity']
            subtotal += item_total
            cart_items.append({
                'id': item['id'],
                'name': item['name'],
                'price': price,
                'price_display': format_price_display(price),
                'image': item['image'],
                'qty': item['quantity'],
                'total': item_total,
                'total_display': format_price_display(item_total)
            })
    
    delivery = 5
    total = subtotal + delivery
    
    return render_template(
        'checkout.html',
        items=cart_items,
        subtotal=subtotal,
        subtotal_display=format_price_display(subtotal),
        delivery=delivery,
        delivery_display=format_price_display(delivery),
        total=total,
        total_display=format_price_display(total)
    )

def newarrivals():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    
    new_arrivals = get_new_arrivals()
    featured_product = new_arrivals[0] if new_arrivals else None
    
    if not featured_product:
        return redirect(url_for('dashboard'))
    
    
    product = {
        **featured_product,
        'category': 'New Arrival',
        'image_url': featured_product.get('image'),
        'title': featured_product.get('name'),
        'description': 'Experience the latest innovation in truck design and performance.'
    }
    
    return render_template('new_arrival.html', product=product)

def productdetails(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    product = get_product_by_id(product_id)
    if not product:
        return redirect(url_for('dashboard'))
    
    
    reviews = [
        {
            "author": "Budi Santoso",
            "date": "Jan 15, 2026",
            "rating": 5,
            "text": "Sangat Bagus Sekali Jangan Bakar Mobil Ku."
        },
        {
            "author": "Jokowi",
            "date": "Jan 12, 2026",
            "rating": 4,
            "text": "Lek seng bener jualnyo."
        },
        {
            "author": "Lek Sawit",
            "date": "Jan 10, 2026",
            "rating": 2,
            "text": "Truk Susah Untuk Jualan Sawit."
        }
    ]
    
    return render_template('product_detail.html', product=product, reviews=reviews)