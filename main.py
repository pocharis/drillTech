from flask import Flask, redirect, render_template, request
from flask_pymongo import pymongo

app = Flask(__name__)

# CONNECTION_STRING = "mongodb+srv://test:test@flask-mongodb-atlas-1g8po.mongodb.net/test?retryWrites=true&w=majority"
# client = pymongo.MongoClient(CONNECTION_STRING)
# db = client.get_database('flask_mongodb_atlas')


client = pymongo.MongoClient("mongodb+srv://abdoul:abdoulonas@pochamb1-50wpb.mongodb.net/drillTechDB?retryWrites=true&w=majority")
db = client.get_database('drillTechDB')
collection = db.drillCalc

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
    collection.delete_many({'calc_type':'ecd'})

    data = collection.find({'calc_type':'ecd'})
    return render_template('ecd.html', data = data)


#route to ecd calculations
@app.route('/drilltech/ecd_calc', methods = ['POST', 'GET'])
def ecd_calc():

    ecd_drill = float(request.form['ecd_drill'])
    mud_weight = int(request.form['mud_weight'])
    depth = int(request.form['depth'])

    surf_equip = int(request.form['surf_equip'])
    in_drill_pipe = int(request.form['in_drill_pipe'])
    in_drill_collars = int(request.form['in_drill_collars'])
    bit_nozzles = int(request.form['bit_nozzles'])
    annulus = int(request.form['annulus'])

    total_pressure = surf_equip +  in_drill_collars + in_drill_pipe + bit_nozzles + annulus
    ecd = round(mud_weight + (annulus / (0.052 * depth)), 2)

    data = {'calc_type':'ecd',
        'ecd_drill': ecd_drill,
        'mud_weight': mud_weight,
        'depth':depth,
        'surf_equip':surf_equip,
        'in_drill_pipe':in_drill_pipe,
        'in_drill_collars':in_drill_collars,
        'bit_nozzles':bit_nozzles,
        'annulus':annulus,
        'ecd':ecd,
        'total_pressure':total_pressure
    }

    collection.insert(data)
    return redirect(url_for('ecd', ecd = ecd, total_pressure = total_pressure ))



if __name__ == '__main__':
    app.run(port=5000,debug=True)

