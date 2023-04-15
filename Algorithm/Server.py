from flask import Flask
from WalletDetails import get_wallet_details
from TransactionDetails import get_transaction_details
from BlackListed import blacklisted
from Predict import predict
from Score import Score
from query import get_address_details
from fetchNodeData import fetch_node
from parseNodeData import parseNodeData
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

# old score based on transactions
@app.route('/predict/<address>')
def predict_score(address):
    with open('./Models/dt_model', 'rb') as f:
        model = pickle.load(f)
    prediction_dataset, total_malicious_tx, malicious_score = predict(address)
    json = {'total_malicious_tx': total_malicious_tx, 'malicious_score': malicious_score}
    return json

# new score based on address
@app.route('/score/<address>')
def score(address):
    score = Score(address)
    print(f"Score:{score}")
    return score
    
@app.route('/blacklisted/<address>')
def is_blacklisted(address):
    isBlackListed = blacklisted(address)
    return isBlackListed

# fetch only outgoing transactions for a given address
@app.route('/tx_out_details/<address>')
def tx_out_details(address):
    details = get_address_details(address)
    return details["data"]["bitcoin"]["outgoing_transactions"]

# get neo4j associated nodes
@app.route('/fetch_node/<address>')
def fetch_node_data(address):
    data = fetch_node(address)
    parsed_data = parseNodeData(data)
    return parsed_data

if __name__ == '__main__':
    app.run(debug=True)