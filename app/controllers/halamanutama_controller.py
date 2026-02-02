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
        return redirect(url_for('home'))

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
    msg = f'{product["name"]} added to cart!'
    # If request is AJAX (fetch), return JSON so client can show popup without redirect
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return { 'success': True, 'message': msg }

    flash(msg, 'success')
    try:
        pid = int(product_id)
    except Exception:
        pid = None

    if pid == 1:
        return redirect(url_for('product_detail', product_id=pid))
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
            
            # Get user_id from username
            cur.execute('SELECT id FROM users WHERE username = %s', (session['username'],))
            user_result = cur.fetchone()
            user_id = user_result[0] if user_result else None
            
            if 'cart' in session:
                for product_id, item in session['cart'].items():
                    quantity = item['quantity']
                    price = parse_price(item['price'])
                    jumlah_pembayaran = price * quantity
                    
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
                        
                        # Insert into history table
                        if user_id:
                            cur.execute('''
                                INSERT INTO history (user_id, produk_id, banyak, jumlah_pembayaran, status_produk)
                                VALUES (%s, %s, %s, %s, %s)
                            ''', (user_id, int(product_id), quantity, jumlah_pembayaran, 'Pending'))
                            print(f"DEBUG: Inserted history for product_id={product_id}", file=sys.stderr)
                    else:
                        print(f"DEBUG: Product not found for product_id={product_id}", file=sys.stderr)
            
            mysql.connection.commit()
            cur.close()
            
            flash('Order placed successfully!', 'success')
            session['cart'] = {}
            session.modified = True
            return redirect(url_for('history'))
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
        return redirect(url_for('home'))
    
    
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
        return redirect(url_for('home'))
    
    
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

def history(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    orders = []
    total_spent = 0
    order_dict = {}
    
    try:
        cur = mysql.connection.cursor()
        
        # Get user_id from username
        cur.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_result = cur.fetchone()
        if not user_result:
            cur.close()
            return render_template('history.html', orders=[], total_spent=0)
        
        user_id = user_result[0]
        
        # Fetch all history entries for this user from the history table
        # Group by date to create orders
        cur.execute('''
            SELECT h.history_id, h.produk_id, h.banyak, h.jumlah_pembayaran, 
                   h.tanggal_pembelian, h.status_produk, p.nama_produk, p.harga
            FROM history h
            JOIN produk p ON h.produk_id = p.produk_id
            WHERE h.user_id = %s
            ORDER BY h.tanggal_pembelian DESC
        ''', (user_id,))
        
        history_rows = cur.fetchall()
        
        # Create separate order entry for each history record
        if history_rows:
            for row in history_rows:
                history_id, produk_id, banyak, jumlah_pembayaran, tanggal_pembelian, status_produk, nama_produk, harga = row
                
                item_total = parse_price(jumlah_pembayaran)
                orders.append({
                    'id': history_id,
                    'date': str(tanggal_pembelian) if tanggal_pembelian else 'Unknown',
                    'status': status_produk or 'sedang dalam pengiriman',
                    'products': [{
                        'id': produk_id,
                        'name': nama_produk,
                        'price': parse_price(harga),
                        'image': 'scania.jpg',
                        'qty': banyak
                    }],
                    'total': item_total
                })
                total_spent += item_total
        
    except Exception as e:
        print(f"DEBUG: Error fetching history: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        orders = []
        total_spent = 0
    
    return render_template(
        'history.html',
        orders=orders,
        total_spent=total_spent
    )