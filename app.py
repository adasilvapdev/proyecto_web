from flask_cors import CORS
from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from flask_mysqldb import MySQL
import sys
from functools import wraps
from threading import Thread

UPLOAD_FOLDER = 'C:/Users\andre/Desktop'
ALLOWED_EXTENSIONS = set(['txt'])

# Configuration
#DEBUG = True

# Instantiate the app
app = Flask(__name__)
app.debug = True

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS
CORS(app)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'properties'
mysql = MySQL(app)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

@app.route('/update_propertie', methods=['POST'])
def update_propertie():  
    propertie_id = request.get_json()['propertie_id']
    description = request.get_json()['description']
    title = request.get_json()['title']
    location = request.get_json()['location']
    status = request.get_json()['status']
    price = request.get_json()['price']    
    
    cur = mysql.connection.cursor()
    cur.execute('UPDATE `properties` SET description = ' + "'" + description + "'" + ', title = ' + "'" + title + "'" + ', location = ' + "'" + location + "'" + ', status = ' + "'" + status + "'" + ', price = ' + "'" + price + "'" + ' WHERE id = ' + str(propertie_id))
    mysql.connection.commit()

    return jsonify({'success': 'success'})

@app.route('/add_propertie', methods=['POST'])
def add_propertie():
    potencial_client_id = request.get_json()['potencial_client_id']
    description = request.get_json()['description']
    title = request.get_json()['title']
    location = request.get_json()['location']
    status = request.get_json()['status']
    price = request.get_json()['price']

    cur = mysql.connection.cursor()

    cur.execute('INSERT INTO properties (potencial_client_id, description, title, location, status, price) VALUES (%s, %s, %s, %s, %s, %s)', (potencial_client_id, description, title, location, status, price))           
    mysql.connection.commit()


    return jsonify({'success': 'success'})

@app.route('/delete_properties', methods=['POST'])
def delete_properties():  
    selected = request.get_json()['selected']
    print("selected: ", selected)
    cur = mysql.connection.cursor()

    for propertie in selected:
        cur.execute('DELETE FROM `properties` WHERE id = ' + str(propertie['id']))
     
    mysql.connection.commit()

    return jsonify({'success': 'success'})

@app.route('/get_properties', methods=['POST'])
def get_properties():  
    _location = request.get_json()['location']
    _status = request.get_json()['status']

    cur = mysql.connection.cursor()

    if _status == None:
        if _location == None:
            to_execute = 'SELECT * FROM properties'
        else:
            to_execute = 'SELECT * FROM properties WHERE location = '+ "'" + _location + "'"
    else:
        if _location == None:
            to_execute = 'SELECT * FROM properties WHERE status = ' + str(_status)
        else:
            to_execute = 'SELECT * FROM properties WHERE status = ' + str(_status) + " AND location = ' "  + _location + "'"
        
    # cur.execute('SELECT * FROM properties WHERE status = ' + str(_status) + " AND location = '" + _location + "'")
    # cur.execute('SELECT * FROM properties')
    cur.execute(to_execute)
    props = cur.fetchall() 
    print("props: ", props)
    mysql.connection.commit()

    properties = []
    for prop in props:
        properties.append({
        'id': prop[0],
        'potencial_client_id': prop[1],
        'description': prop[2],
        'title': prop[3],
        'location': prop[4],
        'status': prop[5],
        'price': prop[6]
    })  

    return jsonify({'properties': properties})

if __name__ == '__main__':
    app.run()