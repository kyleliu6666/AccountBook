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
    title = "All Transactions"
    # Connect to the database
    connection = pymysql.connect(**db_config)
    
    try:
        # Create a cursor object
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Execute SQL query to select all transactions
        cursor.execute("SELECT * FROM Transactions order by TransactionDate")
   
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
    # 可以按需求增加其他的欄位

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "UPDATE Transactions SET Description=%s, Category=%s WHERE TransactionID=%s"
            cursor.execute(sql, (description, category, transaction_id))
            connection.commit()
            return jsonify(success=True), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)