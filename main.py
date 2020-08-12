from flask import Flask, redirect, render_template
from flask_pymongo import pymongo

app = Flask(__name__)

# CONNECTION_STRING = "mongodb+srv://test:test@flask-mongodb-atlas-1g8po.mongodb.net/test?retryWrites=true&w=majority"
# client = pymongo.MongoClient(CONNECTION_STRING)
# db = client.get_database('flask_mongodb_atlas')


client = pymongo.MongoClient("mongodb+srv://abdoul:abdoulonas@pochamb1-50wpb.mongodb.net/drillTechDB?retryWrites=true&w=majority")
db = client.get_database('drillTechDB')


#route to the home page
@app.route('/')
def home():
    return render_template('index.html')


#route to the drill tech page
@app.route('/drilltech')
def drilltech():
    return render_template('drilltech.html')


#route to ecd page
@app.route('/drilltech/ecd')
def ecd():
    collection = db.drillCalc
    data = collection.find({'calc_type':'ecd'})
    return render_template('index.html', data = data)





if __name__ == '__main__':
    app.run(port=5000,debug=True)

