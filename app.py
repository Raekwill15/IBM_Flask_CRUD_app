# Import libraries
from flask import Flask, request, url_for, redirect, render_template
# Instantiate Flask functionality
app = Flask(__name__)


# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]


# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)


# Create operation
@app.route('/add', methods=['GET','POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method == 'POST':
        trans = {
            'id': len(transactions)+1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
                }
        transactions.append(trans)
        return redirect(url_for("get_transactions"))


# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET','POST'])
def edit_transaction(transaction_id):
    if request.method == 'GET':
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template('edit.html', transaction=transaction)
    elif request.method == 'POST':
        newtrans = {'id': transaction_id,
                    'date': request.form['date'],
                    'amount': float(request.form['amount'])
                    }
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transactions[transactions.index(transaction)] = newtrans
                break
        return redirect(url_for('get_transactions'))

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for x in transactions:
        if x['id'] == transaction_id:
            transactions.remove(x)
            break

    return redirect(url_for('get_transactions')) 

@app.route('/search', methods=["GET","POST"])
def search_transactions():
    if request.method == "POST":
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])
        filtered_transactions = [transaction for transaction in transactions if transaction['amount'] > min and transaction['amount'] < max]
        print(filtered_transactions)
        return render_template('transactions.html', transactions = filtered_transactions)
    elif request.method == "GET":
        return render_template('search.html')

@app.route('/balance')
def total_balance():
    sum=0
    for transaction in transactions:
        sum += transaction['amount']
    balance = "Total Balance: " + str(sum) 
    return render_template("transactions.html", transactions=transactions, balance = balance) 

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)