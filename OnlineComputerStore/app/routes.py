# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from app import app
from app.db import get_db_connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['home_address']
        status = request.form['status']
        credit = request.form['credit_amount']

        # Convert blank credit amount to None
        credit = float(credit) if credit else None

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Customer (first_name, last_name, email, phone, home_address, status, credit_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, email, phone, address, status, credit))
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            conn.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')
