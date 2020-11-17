from datetime import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.trade_orders
collection = db.account_status

day1 = {
    "accountid": "None",
    "tradeHistory": 0,
    "accountTotal": 50000.00,
    "btcQuantity": 0,
    "btcBalance": 0.00,
    "usdBalance": 50000.00,
    "dollarSign": "$"
}

collection.insert_one(day1)
print('Success, day1')

## HTML 화면 보기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/order', methods=['POST'])
def save_order():
    type_receive = request.form['type_give']
    price_receive = request.form['price_give']
    count_receive = request.form['count_give']
    total_receive = request.form['total_give']

    doc = {
        'name': type_receive,
        'count': count_receive,
        'price': price_receive,
        'total': total_receive
    }
    print(doc)

    db.trade_orders.insert_one(doc)

    if (type_receive == 'BUY'):
        new_account = collection.find_one({"accountid": "None"})
        new_tradeHistory = new_account['tradeHistory']+1
        new_usdBalance = new_account['accountTotal'] - float(total_receive)
        new_btcQuant = new_account['btcQuantity'] + float(count_receive)
        new_btcBalance = new_btcQuant * float(price_receive)
        new_total = new_usdBalance + new_btcBalance

        collection.update_one({"accountid": "None"},{'$set':{'tradeHistory':new_tradeHistory}}, {'$set':{'accountTotal':new_total}},
                              {'$set':{'btcQuantity':new_btcQuant}}, {'$set':{'btcBalance':new_btcBalance}},
                              {'$set':{'usdBalance':new_usdBalance}})

    else :
        new_account = collection.find_one({"accountid": "None"})
        new_tradeHistory = new_account['tradeHistory']+1
        new_usdBalance = new_account['accountTotal'] + float(total_receive)
        new_btcQuant = new_account['btcQuantity'] - float(count_receive)
        new_btcBalance = new_btcQuant * float(price_receive)
        new_total = new_usdBalance + new_btcBalance

        collection.update_one({"accountid": "None"},{'$set':{'tradeHistory':new_tradeHistory}}, {'$set':{'accountTotal':new_total}},
                              {'$set':{'btcQuantity':new_btcQuant}}, {'$set':{'btcBalance':new_btcBalance}},
                              {'$set':{'usdBalance':new_usdBalance}})


    return jsonify({'result': 'success'})


@app.route('/order', methods=['GET'])
def read_account():

    result = list(collection.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'account': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)