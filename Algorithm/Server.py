from flask import Flask
from WalletDetails import get_wallet_details
from TransactionDetails import get_transaction_details
from BlackListed import blacklisted
from Predict import predict
import pickle

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

@app.route('/predict/<address>')
def predict_score(address):
    with open('./Models/dt_model', 'rb') as f:
        model = pickle.load(f)
    prediction_dataset, total_malicious_tx, malicious_score = predict(address)
    json = {'total_malicious_tx': total_malicious_tx, 'malicious_score': malicious_score}
    return json

@app.route('/blacklisted/<address>')
def is_blacklisted(address):
    isBlackListed = blacklisted(address)
    return isBlackListed

if __name__ == '__main__':
    app.run(debug=True)