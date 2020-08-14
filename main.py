from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import pymongo
import math

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
    # collection.delete_many({'calc_type':'ecd'})

    data = collection.find({'calc_type':'ecd'})
    return render_template('ecd.html', data = data)


#route to ecd calculations
@app.route('/drilltech/ecd_calc', methods = ['POST', 'GET'])
def ecd_calc():

    ecd_drill = float(request.form['ecd_drill'])
    mud_weight = float(request.form['mud_weight'])
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


#route to mud page
@app.route('/drilltech/mud')
def mud():
    # collection.delete_many({'calc_type':'mud'})

    data = collection.find({'calc_type':'mud'})
    return render_template('mud.html', data = data)

#route to ecd calculations
@app.route('/drilltech/mud_calc', methods = ['POST', 'GET'])
def mud_calc():

    ecd_drill = float(request.form['ecd_drill'])
    formation_pres = int(request.form['formation_pres'])
    depth = int(request.form['depth'])
    overbalance_margin = int(request.form['overbalance_margin'])
    

    density = round((0.052 * 10 * depth)/(0.052 * depth), 2)
    
    data = {'calc_type':'mud',
        'ecd_drill': ecd_drill,
        'formation_pres': formation_pres,
        'depth':depth,
        'overbalance_margin':overbalance_margin,
        'density':density,
    }

    collection.insert(data)
    return redirect(url_for('mud', density = density))




#route to leak-off test page
@app.route('/drilltech/leak_off')
def leak_off():
    # collection.delete_many({'calc_type':'leak_off'})

    data = collection.find({'calc_type':'leak_off'})
    return render_template('leak-off.html', data = data)

#route to leak_off calculations
@app.route('/drilltech/leak_off_calc', methods = ['POST', 'GET'])
def leak_off_calc():
    ecd_drill = int(request.form['ecd_drill'])
    leak_off = int(request.form['leak_off'])
    casing_shoe = int(request.form['casing_shoe'])
    mud_weight = float(request.form['mud_weight'])
    

    max_mud_weight = round((leak_off / (0.052 * casing_shoe)) + mud_weight, 2)
    max_breakdown_pressure = round(leak_off + (mud_weight * 0.052 * casing_shoe), 2)
    fracture_gradient = round(max_breakdown_pressure/casing_shoe,2)
    
    data = {'calc_type':'leak_off',
        'ecd_drill': ecd_drill,
        'leak_off': leak_off,
        'casing_shoe': casing_shoe,
        'mud_weight': mud_weight,

        'max_mud_weight':max_mud_weight,
        'max_breakdown_pressure':max_breakdown_pressure,
        'fracture_gradient':fracture_gradient,
    }

    collection.insert(data)
    return redirect(url_for('leak_off', max_mud_weight = max_mud_weight, max_breakdown_pressure = max_breakdown_pressure, fracture_gradient = fracture_gradient))









#route to d-exponent  page
@app.route('/drilltech/d-exponent')
def d_exponent():
    # collection.delete_many({'calc_type':'mud'})

    data = collection.find({'calc_type':'d_exponent'})
    return render_template('d-exponent.html', data = data)

#route to d-exponent calculations
@app.route('/drilltech/d-exponent-calc', methods = ['POST', 'GET'])
def d_exponent_calc():
    rate_of_penetration = int(request.form['rate_of_penetration'])
    rotary_speed = int(request.form['rotary_speed'])
    bit_weight = int(request.form['bit_weight'])
    bit_diameter = float(request.form['bit_diameter'])
    

    d_exponent = -1 * round(math.log10((rate_of_penetration/60) * rotary_speed) / math.log10((12 * bit_weight)/(1000 * bit_diameter)), 2)
    
    data = {'calc_type':'d_exponent',
        'd_exponent': d_exponent,
        'rate_of_penetration': rate_of_penetration,
        'rotary_speed': rotary_speed,
        'bit_weight': bit_weight,
        'bit_diameter': bit_diameter

    }

    collection.insert(data)
    return redirect(url_for('d_exponent', d_exponent = d_exponent))






#route to rheo  page
@app.route('/drilltech/rheo')
def rheo():
    # collection.delete_many({'calc_type':'rheo'})

    data = collection.find({'calc_type':'rheo'})
    return render_template('rheo.html', data = data)

#route to rheo calculations
@app.route('/drilltech/rheo-calc', methods = ['POST', 'GET'])
def rheo_calc():
    rpm600 = int(request.form['rpm600'])
    rpm300 = int(request.form['rpm300'])
    
    

    plastic_viscosity = rpm600 - rpm300
    yeild_point = rpm300 - plastic_viscosity
    
    data = {'calc_type':'rheo',
        'rpm600': rpm600,
        'rpm300': rpm300,
        'plastic_viscosity': plastic_viscosity,
        'yeild_point': yeild_point,
        }

    collection.insert(data)
    return redirect(url_for('rheo', plastic_viscosity = plastic_viscosity, yeild_point = yeild_point))






#route to drill_collar page
@app.route('/drilltech/drill-collar')
def drill_collar():
    # collection.delete_many({'calc_type':'drill_collar_calc'})

    data = collection.find({'calc_type':'drill_collar_calc'})
    return render_template('drill-collar.html', data = data)

#route to drill_collar calculations
@app.route('/drilltech/drill-collar-calc', methods = ['POST', 'GET'])
def drill_collar_calc():
    desired_wob = int(request.form['desired_wob'])
    safety_factor = int(request.form['safety_factor'])
    drill_collar_weight = int(request.form['drill_collar_weight'])
    mud_weight = float(request.form['mud_weight'])
    
    BF = round((65.5 - mud_weight)/65.5,2)
    length_hole_assembly = round((desired_wob * (safety_factor/100))/(drill_collar_weight * BF),3)
    
    data = {'calc_type':'drill_collar_calc',
        'desired_wob': desired_wob,
        'safety_factor': safety_factor,
        'drill_collar_weight': drill_collar_weight,
        'mud_weight': mud_weight,
        'BF':BF,
        'length_hole_assembly':length_hole_assembly
    }

    collection.insert(data)
    return redirect(url_for('drill_collar', BF = BF, length_hole_assembly = length_hole_assembly))




#route to gallery page
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/drillinfo')
def drillinfo():
    return render_template('drillinfo.html')


if __name__ == '__main__':
    app.run(port=5000,debug=True)

