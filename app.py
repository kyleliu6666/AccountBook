from flask import Flask, request, render_template, redirect, url_for
import pymysql
import requests

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
    return render_template('home.html')

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
            
            return 'Transaction added successfully!'
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return 'Form submission failed', 400
    return redirect(url_for('index'))

@app.route('/transactions', methods=['GET'])
def transactions():

    # Connect to the database
    connection = pymysql.connect(**db_config)
    
    try:
        # Create a cursor object
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Execute SQL query to select all transactions
        cursor.execute("SELECT * FROM Transactions")
        
        # Fetch all the records
        transactions = cursor.fetchall()
    finally:
        # Close the database connection
        connection.close()
    
    # Render the transactions template and pass the transactions data
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)