from flask import Flask
from WalletDetails import get_wallet_details
from TransactionDetails import get_transaction_details

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/wallet/<address>')
def wallet_details(address):
    details = get_wallet_details(address)
    # print(details['data'])
    return details['data']

@app.route('/transactions/<address>')
def transaction_details(address):
    details = get_transaction_details(address)
    return details['data']

if __name__ == '__main__':
    app.run(debug=True)