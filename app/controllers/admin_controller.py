from flask import render_template, request, redirect, url_for, session, flash
import matplotlib.pyplot as plt
import os

def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session.get('admin') != 1:
        flash("You do not have admin privileges")
        return redirect(url_for('dashboard'))
    
    return render_template('admin.html', page_title='Dashboard', active_page='dashboard', username=session['username'])

def merk_list(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session.get('admin') != 1:
        flash("You do not have admin privileges")
        return redirect(url_for('dashboard'))
    
    action = request.args.get('action', None)
    merk_id = request.args.get('merk_id', None)
    merk = None
    show_form = False
    
    # Check if form should be shown
    if action == 'create':
        show_form = True
    elif action == 'edit' and merk_id:
        show_form = True
        # Get merk data for editing
        cur = mysql.connection.cursor()
        cur.execute("SELECT merk_id, nama_merk, jumlahpenjualan, keuntungan FROM merk WHERE merk_id = %s", (merk_id,))
        row = cur.fetchone()
        cur.close()
        
        if row:
            merk = {
                'merk_id': row[0],
                'nama_merk': row[1],
                'jumlahpenjualan': row[2],
                'keuntungan': row[3]
            }
        else:
            flash("Merk not found", "error")
    
    # Handle form submission
    if request.method == 'POST':
        nama_merk = request.form.get('nama_merk', '').strip()
        jumlahpenjualan = request.form.get('jumlahpenjualan', 0)
        keuntungan = request.form.get('keuntungan', 0)
        
        if not nama_merk:
            flash("Brand name is required", "error")
            return redirect(url_for('merk_list', action=action, merk_id=merk_id))
        
        try:
            cur = mysql.connection.cursor()
            if merk_id:
                # Update existing
                cur.execute("UPDATE merk SET nama_merk = %s, jumlahpenjualan = %s, keuntungan = %s WHERE merk_id = %s",
                            (nama_merk, jumlahpenjualan, keuntungan, merk_id))
                flash("Merk updated successfully", "success")
            else:
                # Create new
                cur.execute("INSERT INTO merk (nama_merk, jumlahpenjualan, keuntungan) VALUES (%s, %s, %s)",
                            (nama_merk, jumlahpenjualan, keuntungan))
                flash("Merk created successfully", "success")
            
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('merk_list'))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('merk_list', action=action, merk_id=merk_id))
    
    # Get all merks for listing
    cur = mysql.connection.cursor()
    cur.execute("SELECT merk_id, nama_merk, jumlahpenjualan, keuntungan FROM merk ORDER BY merk_id DESC")
    merks_data = cur.fetchall()
    cur.close()
    
    merks = []
    for row in merks_data:
        merks.append({
            'merk_id': row[0],
            'nama_merk': row[1],
            'jumlahpenjualan': row[2],
            'keuntungan': row[3]
        })
    
    # Generate charts
    if merks:
        nama_merk_list = [m['nama_merk'] for m in merks]
        jumlahpenjualan_list = [m['jumlahpenjualan'] for m in merks]
        keuntungan_list = [m['keuntungan'] for m in merks]
        
        # Ensure static directory exists
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        # Bar Chart - Jumlah Penjualan
        plt.figure(figsize=(10, 6))
        plt.bar(nama_merk_list, jumlahpenjualan_list, color='steelblue')
        plt.title('Jumlah Penjualan per Merk')
        plt.xlabel('Nama Merk')
        plt.ylabel('Jumlah Penjualan')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(static_dir, 'merk_bar.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # Pie Chart - Proporsi Penjualan
        plt.figure(figsize=(10, 8))
        plt.pie(jumlahpenjualan_list, labels=nama_merk_list, autopct='%1.1f%%', startangle=90)
        plt.title('Proporsi Penjualan per Merk')
        plt.tight_layout()
        plt.savefig(os.path.join(static_dir, 'merk_pie.png'), dpi=100, bbox_inches='tight')
        plt.close()
    
    return render_template('merk.html', 
                         merks=merks, 
                         merk=merk,
                         show_form=show_form,
                         username=session['username'],
                         page_title='Sales Management - Merk',
                         active_page='sales')

def merk_delete(mysql, merk_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session.get('admin') != 1:
        flash("You do not have admin privileges")
        return redirect(url_for('dashboard'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM merk WHERE merk_id = %s", (merk_id,))
        mysql.connection.commit()
        cur.close()
        
        flash("Merk deleted successfully", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    
    return redirect(url_for('merk_list'))

def customer_list(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session.get('admin') != 1:
        flash("You do not have admin privileges")
        return redirect(url_for('dashboard'))
    
    # Get all non-admin users
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, first_name, last_name, email, phone, address FROM users WHERE admin = 0 ORDER BY id DESC")
    customers_data = cur.fetchall()
    cur.close()
    
    customers = []
    for row in customers_data:
        customers.append({
            'id': row[0],
            'username': row[1],
            'first_name': row[2],
            'last_name': row[3],
            'email': row[4],
            'phone': row[5],
            'address': row[6]
        })
    
    return render_template('customers.html', 
                         customers=customers, 
                         username=session['username'],
                         page_title='Customers Management',
                         active_page='customers')

