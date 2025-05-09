# app/routes_user.py
from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.db import get_db_connection
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Customer (first_name, last_name, email, password)
                VALUES (%s, %s, %s, %s)
            """, (fname, lname, email, hashed_password))
            conn.commit()
            flash('User registration successful! Please login.', 'success')
            return redirect(url_for('user_login'))
        except Exception as e:
            conn.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('user_register.html')



@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Customer WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('shop'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('user_login.html')


@app.route('/user/logout')
def user_logout():
    session.pop('user_email', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('user_login'))



# Helper function to get customer_id
def get_customer_id(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM Customer WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# ================== SHOPPING ==================

@app.route('/shop')
def shop():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user_email = session.get('user_email')
    customer_status = 'regular'  # default for guests

    if user_email:
        cursor.execute("SELECT status FROM Customer WHERE email = %s", (user_email,))
        result = cursor.fetchone()
        if result:
            customer_status = result['status']

    if customer_status in ['gold', 'platinum']:
        # Gold & Platinum users get special offer prices if available
        cursor.execute("""
            SELECT 
                p.product_id, p.name,
                COALESCE(so.offer_price, p.recommended_price) AS final_price,
                p.recommended_price,
                p.quantity_in_stock
            FROM Product p
            LEFT JOIN SpecialOffer so ON p.product_id = so.product_id
            WHERE p.quantity_in_stock > 0
        """)
    else:
        # Regular & Silver see only the recommended price
        cursor.execute("""
            SELECT 
                product_id, name,
                recommended_price AS final_price,
                recommended_price,
                quantity_in_stock
            FROM Product
            WHERE quantity_in_stock > 0
        """)

    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('shop.html', products=products, customer_status=customer_status)


@app.route('/cart/add/<int:product_id>')
def cart_add(product_id):
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create or find the user's basket
    cursor.execute("SELECT basket_id FROM ShoppingBasket WHERE customer_id = %s", (customer_id,))
    basket = cursor.fetchone()
    if not basket:
        cursor.execute("INSERT INTO ShoppingBasket (customer_id) VALUES (%s)", (customer_id,))
        conn.commit()
        basket_id = cursor.lastrowid
    else:
        basket_id = basket[0]

    # Insert or update cart item
    cursor.execute("""
        INSERT INTO ShoppingCartItem (basket_id, product_id, quantity)
        VALUES (%s, %s, 1)
        ON DUPLICATE KEY UPDATE quantity = quantity + 1
    """, (basket_id, product_id))
    conn.commit()

    cursor.close()
    conn.close()
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT ci.cart_item_id, p.name, p.product_id, ci.quantity, p.recommended_price
    FROM ShoppingBasket sb
    JOIN ShoppingCartItem ci ON sb.basket_id = ci.basket_id
    JOIN Product p ON ci.product_id = p.product_id
    WHERE sb.customer_id = %s
""", (customer_id,))
    cart_items = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/cart/remove/<int:product_id>')
def cart_remove(product_id):
    if 'user_email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor()

    # Corrected to target ShoppingCartItem
    cursor.execute("""
        DELETE sci
        FROM ShoppingCartItem sci
        JOIN ShoppingBasket sb ON sci.basket_id = sb.basket_id
        WHERE sb.customer_id = %s AND sci.product_id = %s
    """, (customer_id, product_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Product removed from cart.', 'success')
    return redirect(url_for('cart'))


# ================== CHECKOUT ==================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user's cards
    cursor.execute("SELECT * FROM CreditCard WHERE customer_id = %s", (customer_id,))
    cards = cursor.fetchall()

    # Fetch user's shipping addresses
    cursor.execute("SELECT * FROM ShippingAddress WHERE customer_id = %s", (customer_id,))
    addresses = cursor.fetchall()

    if request.method == 'POST':
        card_number = request.form['card_number']
        address_name = request.form['address_name']

        # Find user's basket
        cursor.execute("SELECT basket_id FROM ShoppingBasket WHERE customer_id = %s", (customer_id,))
        basket = cursor.fetchone()

        if not basket:
            flash('No active basket.', 'danger')
            return redirect(url_for('shop'))
        
        basket_id = basket['basket_id']

        # Create SalesTransaction
        cursor.execute("""
            INSERT INTO SalesTransaction (basket_id, card_number, shipping_customer_id, shipping_address_name, total_amount)
            VALUES (%s, %s, %s, %s, 0)
        """, (basket_id, card_number, customer_id, address_name))
        conn.commit()
        transaction_id = cursor.lastrowid

        # Move cart items into TransactionDetails
        cursor.execute("""
            SELECT ci.product_id, ci.quantity, p.recommended_price
            FROM ShoppingCartItem ci
            JOIN Product p ON ci.product_id = p.product_id
            WHERE ci.basket_id = %s
        """, (basket_id,))
        cart_items = cursor.fetchall()

        total_amount = 0

        for item in cart_items:
            final_price = item['recommended_price'] * item['quantity']
            total_amount += final_price

            cursor.execute("""
                INSERT INTO TransactionDetails (transaction_id, product_id, quantity, final_price)
                VALUES (%s, %s, %s, %s)
            """, (transaction_id, item['product_id'], item['quantity'], item['recommended_price']))

        # Update total_amount
        cursor.execute("""
            UPDATE SalesTransaction
            SET total_amount = %s
            WHERE transaction_id = %s
        """, (total_amount, transaction_id))

        # Clear cart
        cursor.execute("DELETE FROM ShoppingCartItem WHERE basket_id = %s", (basket_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Checkout completed successfully.', 'success')
        return redirect(url_for('shop'))

    cursor.close()
    conn.close()

    return render_template('checkout.html', cards=cards, addresses=addresses)




# ================== SHIPPING ADDRESS MANAGEMENT ==================

@app.route('/profile/shippingaddresses')
def shippingaddress_list():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ShippingAddress WHERE customer_id = %s", (customer_id,))
    addresses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('shippingaddress_list.html', addresses=addresses)

@app.route('/profile/shippingaddresses/add', methods=['GET', 'POST'])
def shippingaddress_add():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])

    if request.method == 'POST':
        address_name = request.form['address_name']
        zip_code = request.form['zip_code']
        street_name = request.form['street_name']
        street_number = request.form['street_number']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ShippingAddress (customer_id, address_name, zip_code, street_name, street_number, city, state, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (customer_id, address_name, zip_code, street_name, street_number, city, state, country))
            conn.commit()
            flash('Shipping address added successfully.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to add address: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('shippingaddress_list'))

    return render_template('shippingaddress_add.html')

@app.route('/profile/shippingaddresses/delete/<address_name>')
def shippingaddress_delete(address_name):
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM ShippingAddress
        WHERE customer_id = %s AND address_name = %s
    """, (customer_id, address_name))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Shipping address deleted.', 'success')
    return redirect(url_for('shippingaddress_list'))


# ================== ORDERS ===================

@app.route('/profile/orders')
def order_list():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT st.transaction_id, st.total_amount, st.status, st.transaction_date
        FROM SalesTransaction st
        WHERE st.shipping_customer_id = %s
        ORDER BY st.transaction_date DESC
    """, (customer_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('order_list.html', orders=orders)


@app.route('/profile/orders/<int:transaction_id>')
def user_order_detail(transaction_id):
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Confirm that this order belongs to the user
    cursor.execute("""
        SELECT * FROM SalesTransaction
        WHERE transaction_id = %s AND shipping_customer_id = %s
    """, (transaction_id, customer_id))
    transaction = cursor.fetchone()

    if not transaction:
        cursor.close()
        conn.close()
        flash('Transaction not found.', 'danger')
        return redirect(url_for('order_list'))

    # Fetch products in this transaction
    cursor.execute("""
        SELECT td.product_id, p.name, td.quantity, td.final_price
        FROM TransactionDetails td
        JOIN Product p ON td.product_id = p.product_id
        WHERE td.transaction_id = %s
    """, (transaction_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('order_detail.html', transaction=transaction, items=items)


# ================== PROFILE ==================

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Handle update
    if request.method == 'POST':
        phone = request.form['phone']
        address = request.form['home_address']
        cursor.execute("""
            UPDATE Customer
            SET phone = %s, home_address = %s
            WHERE customer_id = %s
        """, (phone, address, customer_id))
        conn.commit()
        flash('Profile updated.', 'success')

    # Fetch profile, addresses, and cards
    cursor.execute("SELECT * FROM Customer WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()

    cursor.execute("SELECT * FROM ShippingAddress WHERE customer_id = %s", (customer_id,))
    addresses = cursor.fetchall()

    cursor.execute("SELECT * FROM CreditCard WHERE customer_id = %s", (customer_id,))
    cards = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('profile.html', customer=customer, addresses=addresses, cards=cards)


@app.route('/profile/creditcards/add', methods=['GET', 'POST'])
def creditcard_add():
    if 'user_email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    if request.method == 'POST':
        card_number = request.form['card_number']
        security_code = request.form['security_code']
        owner_name = request.form['owner_name']
        billing_address = request.form['billing_address']
        card_type = request.form['card_type']
        expiry_date = request.form['expiry_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CreditCard (card_number, customer_id, security_code, owner_name, billing_address, card_type, expiry_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (card_number, customer_id, security_code, owner_name, billing_address, card_type, expiry_date))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Credit card added successfully.', 'success')
        return redirect(url_for('profile'))

    return render_template('creditcard_add.html')

@app.route('/profile/creditcards/delete/<card_number>')
def creditcard_delete(card_number):
    if 'user_email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM CreditCard
        WHERE card_number = %s AND customer_id = %s
    """, (card_number, customer_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Credit card deleted successfully.', 'success')
    return redirect(url_for('profile'))

@app.route('/profile/shippingaddresses/edit/<address_name>', methods=['GET', 'POST'])
def shippingaddress_edit(address_name):
    if 'user_email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        zip_code = request.form['zip_code']
        street_name = request.form['street_name']
        street_number = request.form['street_number']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        cursor.execute("""
            UPDATE ShippingAddress
            SET zip_code = %s, street_name = %s, street_number = %s,
                city = %s, state = %s, country = %s
            WHERE customer_id = %s AND address_name = %s
        """, (zip_code, street_name, street_number, city, state, country, customer_id, address_name))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Shipping address updated.', 'success')
        return redirect(url_for('profile'))

    # GET method — fetch the address to edit
    cursor.execute("""
        SELECT * FROM ShippingAddress
        WHERE customer_id = %s AND address_name = %s
    """, (customer_id, address_name))
    address = cursor.fetchone()

    cursor.close()
    conn.close()

    if not address:
        flash('Shipping address not found.', 'danger')
        return redirect(url_for('profile'))

    return render_template('shippingaddress_edit.html', address=address)



@app.route('/profile/creditcards/edit/<card_number>', methods=['GET', 'POST'])
def creditcard_edit(card_number):
    if 'user_email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('user_login'))

    customer_id = get_customer_id(session['user_email'])
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        owner_name = request.form['owner_name']
        billing_address = request.form['billing_address']
        card_type = request.form['card_type']
        expiry_date = request.form['expiry_date']

        cursor.execute("""
            UPDATE CreditCard
            SET owner_name = %s, billing_address = %s, card_type = %s, expiry_date = %s
            WHERE card_number = %s AND customer_id = %s
        """, (owner_name, billing_address, card_type, expiry_date, card_number, customer_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Credit card updated.', 'success')
        return redirect(url_for('profile'))

    cursor.execute("""
        SELECT * FROM CreditCard
        WHERE card_number = %s AND customer_id = %s
    """, (card_number, customer_id))
    card = cursor.fetchone()
    cursor.close()
    conn.close()

    if not card:
        flash('Credit card not found.', 'danger')
        return redirect(url_for('profile'))

    return render_template('creditcard_edit.html', card=card)
