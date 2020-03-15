from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'rent'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rent'

mongo = PyMongo(app)

@app.route('/rent/lg', methods=['GET'])
def get_rent_location_gender():
    rent = mongo.db.pageContent
    location = '新北'
    gender = '男'
    output = []
    result =  rent.find({'$and':[{'row.title': { '$regex' : location }, 'row.性別要求':{ '$regex' : gender }}]} )
    for s in result:
        output.append ({'row' : s['row']})
    return jsonify({'result' : output})

@app.route('/rent', methods=['GET'])
def get_rents_by_phone():
    rent = mongo.db.pageContent
    phone_num = request.args.get('phone',None)
    output = []
    for s in rent.find({'row.電話' :{'$regex': phone_num}}):
        output.append({'row' : s['row']})
    return jsonify({'result' : output})

@app.route('/rent/post-by-others', methods=['GET'])
def get_rents_post_by_others():
    rent = mongo.db.pageContent
    output = []
    for s in rent.find({'row.身分':{ '$not':{ '$regex':'屋主'}}}):
        output.append({'row' : s['row']})
    return jsonify({'result' : output})

@app.route('/rent/tp-mswu-own', methods=['GET'])
def get_rents_mswu_self_tp():
    rent = mongo.db.pageContent
    output = []
    f_owner ={'row.身分':{'$regex':'屋主'}}
    f_wu={'row.稱謂':{'$regex':'吳'}}
    f_ms = {'$or':[{'row.稱謂':{'$regex':'小姐'}},{'row.稱謂':{'$regex':'太太'}}]}

    f_all = {'$and':[f_owner,f_wu,f_ms]}

    for s in rent.find(f_all):
        output.append({'row' : s['row']})

    return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)
