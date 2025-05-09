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
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Admin (username, password)
                VALUES (%s, %s)
            """, (email, password))
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
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE username = %s AND password = %s", (email, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            session['admin_user'] = email
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
    if 'admin_user' not in session:
        flash('Please log in as admin to continue.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the product is referenced in any transaction
        cursor.execute("""
            SELECT COUNT(*) FROM TransactionDetails WHERE product_id = %s
        """, (product_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            flash("❌ Cannot delete this product because it has been sold in transactions.", "danger")
        else:
            # Safe to delete
            cursor.execute("DELETE FROM Product WHERE product_id = %s", (product_id,))
            conn.commit()
            flash("✅ Product deleted successfully.", "success")

    except Exception as e:
        conn.rollback()
        flash(f"⚠️ Error deleting product: {str(e)}", "danger")

    finally:
        cursor.close()
        conn.close()

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


# ================== CUSTOMER MANAGEMENT ===================

@app.route('/admin/customers', methods=['GET', 'POST'])
def admin_customers():
    if 'admin_user' not in session:
        flash('Please log in as admin to continue.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        new_status = request.form.get('new_status')
        print("➡️ Received POST: customer_id =", customer_id, "| new_status =", new_status)

        try:
            cursor.execute("""
                UPDATE Customer SET status = %s WHERE customer_id = %s
            """, (new_status, customer_id))

            print("⬅️ Rows affected:", cursor.rowcount)

            conn.commit()
            flash('✅ Customer status updated successfully.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f"⚠️ Failed to update status: {str(e)}", 'danger')

    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_customers.html', customers=customers)





# ================== PROMOTION MANAGEMENT ==================

@app.route('/admin/promotions')
def admin_promotions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT SpecialOffer.offer_id,
           Product.name AS product_name,
           SpecialOffer.offer_price,
           SpecialOffer.allowed_status
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
        allowed_status = request.form['allowed_status'] or None

        cursor.execute("""
            INSERT INTO SpecialOffer (product_id, offer_price, allowed_status)
            VALUES (%s, %s, %s)
        """, (product_id, offer_price, allowed_status))
        conn.commit()
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
        allowed_status = request.form['allowed_status'] or None

        cursor.execute("""
            UPDATE SpecialOffer
            SET offer_price = %s, allowed_status = %s
            WHERE offer_id = %s
        """, (offer_price, allowed_status, offer_id))
        conn.commit()
        flash('Promotion updated successfully!', 'success')
        return redirect(url_for('admin_promotions'))

    else:
        cursor.execute("""
            SELECT s.offer_id, s.offer_price, s.allowed_status,
                   p.name AS product_name
            FROM SpecialOffer s
            JOIN Product p ON s.product_id = p.product_id
            WHERE s.offer_id = %s
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


@app.route('/admin/orders/<int:transaction_id>/update_status', methods=['POST'])
def admin_update_order_status(transaction_id):
    new_status = request.form['new_status']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE SalesTransaction
        SET status = %s
        WHERE transaction_id = %s
    """, (new_status, transaction_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Order status updated successfully.', 'success')
    return redirect(url_for('admin_order_detail', transaction_id=transaction_id))


# ====================== STATISTICS ====================================

@app.route('/admin/statistics')
def admin_statistics_dashboard():
    return render_template('admin_statistics.html')



@app.route('/admin/statistics/total_by_card')
def admin_total_by_card():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT card_number, SUM(total_amount) as total_charged
        FROM SalesTransaction
        GROUP BY card_number
        ORDER BY total_charged DESC
    """)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_total_by_card.html', results=results)


@app.route('/admin/statistics/top_customers')
def admin_top_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.customer_id, c.first_name, c.last_name, SUM(st.total_amount) AS total_spent
        FROM SalesTransaction st
        JOIN Customer c ON st.shipping_customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
        LIMIT 10
    """)
    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_top_customers.html', customers=customers)


@app.route('/admin/statistics/most_sold_products', methods=['GET', 'POST'])
def admin_most_sold_products():
    products = []

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.name, SUM(td.quantity) AS total_sold
            FROM TransactionDetails td
            JOIN Product p ON td.product_id = p.product_id
            JOIN SalesTransaction st ON td.transaction_id = st.transaction_id
            WHERE st.transaction_date BETWEEN %s AND %s
            GROUP BY p.product_id
            ORDER BY total_sold DESC
        """, (start_date, end_date))
        products = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('admin_most_sold_products.html', products=products)


@app.route('/admin/statistics/products_by_customers', methods=['GET', 'POST'])
def admin_products_by_customers():
    products = []

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.name, COUNT(DISTINCT st.shipping_customer_id) AS distinct_customers
            FROM TransactionDetails td
            JOIN Product p ON td.product_id = p.product_id
            JOIN SalesTransaction st ON td.transaction_id = st.transaction_id
            WHERE st.transaction_date BETWEEN %s AND %s
            GROUP BY p.product_id
            ORDER BY distinct_customers DESC
        """, (start_date, end_date))
        products = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('admin_products_by_customers.html', products=products)


@app.route('/admin/statistics/max_basket_per_card', methods=['GET', 'POST'])
def admin_max_basket_per_card():
    cards = []

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT card_number, MAX(total_amount) AS max_basket
            FROM SalesTransaction
            WHERE transaction_date BETWEEN %s AND %s
            GROUP BY card_number
            ORDER BY max_basket DESC
        """, (start_date, end_date))
        cards = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('admin_max_basket_per_card.html', cards=cards)


@app.route('/admin/statistics/avg_price_per_type', methods=['GET', 'POST'])
def admin_avg_price_per_type():
    averages = []

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT pt.category, AVG(td.final_price) AS avg_price
            FROM TransactionDetails td
            JOIN Product p ON td.product_id = p.product_id
            JOIN ProductType pt ON p.type_id = pt.type_id
            JOIN SalesTransaction st ON td.transaction_id = st.transaction_id
            WHERE st.transaction_date BETWEEN %s AND %s
            GROUP BY pt.category
        """, (start_date, end_date))
        averages = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('admin_avg_price_per_type.html', averages=averages)

