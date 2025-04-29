from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.db import get_db_connection


@app.route('/admin/home')
def admin_home():
    if 'admin_user' not in session:
        flash('Please login as admin.', 'danger')
        return redirect(url_for('admin_login'))
    return render_template('admin_home.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Admin (username, password)
                VALUES (%s, %s)
            """, (username, password))
            conn.commit()
            flash('Admin registered successfully!', 'success')
            return redirect(url_for('admin_login'))
        except Exception as e:
            conn.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('admin_register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            session['admin_user'] = username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('admin_login.html')



# ================== PRODUCT MANAGEMENT ==================

@app.route('/admin/products')
def admin_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_product_add():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT type_id, name FROM ProductType")
    types = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['recommended_price']
        quantity = request.form['quantity_in_stock']
        type_id = request.form['type_id']

        cursor.execute("""
            INSERT INTO Product (name, description, recommended_price, quantity_in_stock, type_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, price, quantity, type_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))

    cursor.close()
    conn.close()
    return render_template('admin_product_add.html', types=types)


@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def admin_product_edit(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['recommended_price']
        quantity = request.form['quantity_in_stock']
        type_id = request.form['type_id']
        cursor.execute("""
            UPDATE Product
            SET name=%s, description=%s, recommended_price=%s, quantity_in_stock=%s, type_id=%s
            WHERE product_id=%s
        """, (name, description, price, quantity, type_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    else:
        cursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('admin_product_edit.html', product=product)

@app.route('/admin/products/delete/<int:product_id>')
def admin_product_delete(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Product WHERE product_id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/producttypes/add', methods=['GET', 'POST'])
def admin_producttype_add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        cpu_type = request.form.get('cpu_type')
        weight = request.form.get('weight')
        battery_life = request.form.get('battery_life')
        resolution = request.form.get('resolution')
        printer_type = request.form.get('printer_type')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ProductType (name, category, cpu_type, weight, battery_life, resolution, printer_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, category, cpu_type, weight, battery_life, resolution, printer_type))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Product Type added successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin_producttype_add.html')


# ================== PROMOTION MANAGEMENT ==================

@app.route('/admin/promotions')
def admin_promotions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT SpecialOffer.offer_id, Product.name AS product_name, SpecialOffer.offer_price
        FROM SpecialOffer
        JOIN Product ON SpecialOffer.product_id = Product.product_id
    """)
    promotions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_promotions.html', promotions=promotions)

@app.route('/admin/promotions/add', methods=['GET', 'POST'])
def admin_promotion_add():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_id, name FROM Product")
    products = cursor.fetchall()

    if request.method == 'POST':
        product_id = request.form['product_id']
        offer_price = request.form['offer_price']
        cursor.execute("""
            INSERT INTO SpecialOffer (product_id, offer_price)
            VALUES (%s, %s)
        """, (product_id, offer_price))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Promotion added successfully!', 'success')
        return redirect(url_for('admin_promotions'))

    cursor.close()
    conn.close()
    return render_template('admin_promotion_add.html', products=products)

@app.route('/admin/promotions/edit/<int:offer_id>', methods=['GET', 'POST'])
def admin_promotion_edit(offer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        offer_price = request.form['offer_price']
        cursor.execute("""
            UPDATE SpecialOffer
            SET offer_price=%s
            WHERE offer_id=%s
        """, (offer_price, offer_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Promotion updated successfully!', 'success')
        return redirect(url_for('admin_promotions'))

    else:
        cursor.execute("""
            SELECT SpecialOffer.offer_id, Product.name AS product_name, SpecialOffer.offer_price
            FROM SpecialOffer
            JOIN Product ON SpecialOffer.product_id = Product.product_id
            WHERE SpecialOffer.offer_id = %s
        """, (offer_id,))
        promotion = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('admin_promotion_edit.html', promotion=promotion)

@app.route('/admin/promotions/delete/<int:offer_id>')
def admin_promotion_delete(offer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SpecialOffer WHERE offer_id = %s", (offer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Promotion deleted successfully!', 'success')
    return redirect(url_for('admin_promotions'))

# ======================= ORDER MANAGEMENT ======================

@app.route('/admin/orders/search', methods=['GET', 'POST'])
def admin_order_search():
    if request.method == 'POST':
        search_type = request.form['search_type']
        search_value = request.form['search_value']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if search_type == 'email':
            cursor.execute("""
                SELECT st.transaction_id, st.total_amount, st.status, st.transaction_date
                FROM SalesTransaction st
                JOIN Customer c ON st.shipping_customer_id = c.customer_id
                WHERE c.email = %s
            """, (search_value,))
        else:  # customer_id
            cursor.execute("""
                SELECT transaction_id, total_amount, status, transaction_date
                FROM SalesTransaction
                WHERE shipping_customer_id = %s
            """, (search_value,))

        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('admin_order_search.html', orders=orders)

    return render_template('admin_order_search.html')

@app.route('/admin/orders/<int:transaction_id>')
def admin_order_detail(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM SalesTransaction WHERE transaction_id = %s
    """, (transaction_id,))
    transaction = cursor.fetchone()

    if not transaction:
        cursor.close()
        conn.close()
        flash('Transaction not found.', 'danger')
        return redirect(url_for('admin_home'))

    cursor.execute("""
        SELECT td.product_id, p.name, td.quantity, td.final_price
        FROM TransactionDetails td
        JOIN Product p ON td.product_id = p.product_id
        WHERE td.transaction_id = %s
    """, (transaction_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_order_detail.html', transaction=transaction, items=items)
