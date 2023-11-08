from flask import Flask, request, render_template, redirect, url_for , flash,jsonify
import pymysql
import requests
from datetime import date

app = Flask(__name__)


# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'password',
    'database': 'MyAccountBook'
}

# Route to display the form
@app.route('/')
def index():
    title = "AccountBook"
    return render_template('home.html', title=title)

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
            
            return redirect(url_for('index'))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return 'Form submission failed', 400
    return redirect(url_for('transactions'))

@app.route('/transactions', methods=['GET'])
def transactions():
    title = "Day Transactions"
    # Connect to the database
    connection = pymysql.connect(**db_config)
    
    try:
        # Create a cursor object
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Execute SQL query to select all transactions
        cursor.execute("SELECT * FROM Transactions WHERE DATE(TransactionDate) = CURDATE() ORDER BY TransactionDate DESC;")
   
        # Fetch all the records
        transactions = cursor.fetchall()
    finally:
        # Close the database connection
        connection.close()
    
    # Render the transactions template and pass the transactions data
    return render_template('transactions.html', transactions=transactions,title=title)

@app.route('/month_transactions', methods=['GET'])
def month_transactions():
    title = "Month Transactions"
    # Connect to the database
    connection = pymysql.connect(**db_config)
    
    try:
        # Create a cursor object
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Execute SQL query to select all transactions
        cursor.execute("SELECT * FROM Transactions WHERE TransactionDate BETWEEN CURDATE() - INTERVAL 1 MONTH AND CURDATE() ORDER BY TransactionDate DESC;")
   
        # Fetch all the records
        transactions = cursor.fetchall()
    finally:
        # Close the database connection
        connection.close()
    
    # Render the transactions template and pass the transactions data
    return render_template('transactions.html', transactions=transactions,title=title)

@app.route('/year_transactions', methods=['GET'])
def year_transactions():
    title = "Year Transactions"
    # Connect to the database
    connection = pymysql.connect(**db_config)
    
    try:
        # Create a cursor object
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Execute SQL query to select all transactions
        cursor.execute("SELECT * FROM Transactions WHERE TransactionDate BETWEEN CURDATE() - INTERVAL 1 YEAR AND CURDATE() ORDER BY TransactionDate DESC;")
   
        # Fetch all the records
        transactions = cursor.fetchall()
    finally:
        # Close the database connection
        connection.close()
    
    # Render the transactions template and pass the transactions data
    return render_template('transactions.html', transactions=transactions,title=title)

@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "DELETE FROM Transactions WHERE TransactionID = %s"
            cursor.execute(sql, (transaction_id,))
            connection.commit()
            if cursor.rowcount:
                flash('Transaction deleted successfully.', 'success')
            else:
                flash('Transaction not found.', 'error')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
    finally:
        return redirect(url_for('transactions'))


@app.route('/update/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
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

    values.append(transaction_id)

    # 如果沒有任何欄位需要更新，則直接返回
    if not fields:
        return jsonify(error="No fields provided to update"), 400

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "UPDATE Transactions SET " + ", ".join(fields) + " WHERE TransactionID=%s"
            cursor.execute(sql, tuple(values))
            connection.commit()
            return jsonify(success=True), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        connection.close()



if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)