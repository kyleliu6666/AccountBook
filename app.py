from flask import Flask, request, render_template, redirect, url_for , flash,jsonify
import pymysql
import requests
from datetime import date
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Database configuration
db_config = {
    'host': os.getenv("DB_IP"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PW"),
    'database': os.getenv("DB_NAME")
}

# Route to display the form
@app.route('/')
def index():
    return redirect('/new')

@app.route('/new')
def new():
    title = "Spendalytics"
    connection = pymysql.connect(**db_config)
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM MyAccountBook.TransactionTemplates;")
        templates = cursor.fetchall()
    finally:
        connection.close()
    return render_template('new.html', title=title, templates=templates)

@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            # Get data from form
            date = request.form['date']
            category = request.form['category']
            description = request.form['description']
            amount = request.form['amount']
            type = request.form['type']
            payment_method = request.form['payment_method']
            merchant = request.form['merchant']
            location = request.form['location']
            
            
            # Insert data into database
            connection = pymysql.connect(**db_config)
            try:
                with connection.cursor() as cursor:
                    sql = '''
                        INSERT INTO Transactions (TransactionDate, Category, Description, Amount, TransactionType, PaymentMethod, Merchant, Location)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(sql, (date, category, description, amount, type, payment_method, merchant, location))
                connection.commit()
            finally:
                connection.close()
            
            return redirect(url_for('transactions'))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return 'Form submission failed', 400
    return redirect(url_for('transactions'))

@app.route('/templates', methods=['GET'])
def templates():
    title = "Templates"
    connection = pymysql.connect(**db_config)
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM MyAccountBook.TransactionTemplates;")
        transactions = cursor.fetchall()
    finally:
        connection.close()

    return render_template('templates.html', transactions=transactions,title=title)

@app.route('/transactions', methods=['GET'])
def transactions():
    title = "Day Transactions"
    connection = pymysql.connect(**db_config)
    
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM Transactions WHERE DATE(TransactionDate) = CURDATE() ORDER BY TransactionDate DESC;")
   
        transactions = cursor.fetchall()

        cursor.execute("SELECT SUM(Amount) AS total_spent FROM Transactions WHERE DATE(TransactionDate) = CURDATE();")

        result = cursor.fetchone()['total_spent']
        if result is None:
            total_spent = 0  # 或適當的預設值
        else:
            total_spent = round(result)


    finally:
        connection.close()
    
    return render_template('transactions.html', transactions=transactions,total_spent=total_spent,title=title)

@app.route('/month_transactions', methods=['GET'])
def month_transactions():
    title = "Month Transactions"
    connection = pymysql.connect(**db_config)
    
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM Transactions WHERE MONTH(TransactionDate) = MONTH(CURDATE()) AND YEAR(TransactionDate) = YEAR(CURDATE()) ORDER BY TransactionDate DESC;")
   
        transactions = cursor.fetchall()

        cursor.execute("SELECT SUM(Amount) AS total_spent FROM Transactions WHERE MONTH(TransactionDate) = MONTH(CURDATE()) AND YEAR(TransactionDate) = YEAR(CURDATE());")
        
        result = cursor.fetchone()['total_spent']
        if result is None:
            total_spent = 0  # 或適當的預設值
        else:
            total_spent = round(result)

    finally:
        connection.close()

    return render_template('transactions.html', transactions=transactions,total_spent=total_spent,title=title)

@app.route('/year_transactions', methods=['GET'])
def year_transactions():
    title = "Year Transactions"
    connection = pymysql.connect(**db_config)
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM MyAccountBook.Transactions WHERE TransactionDate >= MAKEDATE(YEAR(CURDATE()), 1) AND TransactionDate <= CURDATE() ORDER BY TransactionDate DESC;")
        transactions = cursor.fetchall()

        cursor.execute("SELECT SUM(Amount) AS total_spent FROM Transactions WHERE YEAR(TransactionDate) = YEAR(CURDATE());")

        result = cursor.fetchone()['total_spent']
        if result is None:
            total_spent = 0  # 或適當的預設值
        else:
            total_spent = round(result)


    finally:
        connection.close()
    
    return render_template('transactions.html', transactions=transactions,total_spent=total_spent,title=title)

@app.route('/delete_template/<int:template_id>', methods=['POST'])
def delete_template(template_id):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "DELETE FROM TransactionTemplates WHERE TemplateID = %s"
            cursor.execute(sql, (template_id,))
            connection.commit()
            if cursor.rowcount:
                flash('Template deleted successfully.', 'success')
            else:
                flash('Template not found.', 'error')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
    finally:
        return redirect(url_for('templates'))

@app.route('/update_template/<int:template_id>', methods=['POST'])
def update_template(template_id):
    description = request.form.get('description')
    category = request.form.get('category')

    fields = []
    values = []

    if description is not None:
        fields.append("Description=%s")
        values.append(description)
    
    if category is not None:
        fields.append("Category=%s")
        values.append(category)

    values.append(template_id)

    # 如果沒有任何欄位需要更新，則直接返回
    if not fields:
        return jsonify(error="No fields provided to update"), 400

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "UPDATE TransactionTemplates SET " + ", ".join(fields) + " WHERE TemplateID=%s"
            cursor.execute(sql, tuple(values))
            connection.commit()
            return jsonify(success=True), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        connection.close()



if __name__ == '__main__':
     app.run(host='0.0.0.0', port=os.getenv("SERVICE_PORT"))
