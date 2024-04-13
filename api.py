from flask import Flask, jsonify, request
from pymongo import MongoClient
import re

app = Flask(__name__)

def open_mongo_db():
    """" It opens the connection with the mongo db.
    There after we can close it in every function, using client.close()"""
    try:
        client = MongoClient('mongodb+srv://mverad:mverad@cluster0.uavhcn6.mongodb.net/')
        db = client['Agenda']
        coll = db['Agenda']
    except Exception as e:
        print(f'Error: {e}')
    return coll, client
    
@app.route('/buscar', methods=['POST'])
def look_up_contact():
    """ Function returns the result of looking up for a contact by name"""
    coll, client = open_mongo_db()
    name = request.args.get('nombre', type=str)
    regex_pattern = f'.*{re.escape(name)}.*'
    result = list(coll.find({'nombre': {'$regex': regex_pattern, '$options': 'i'}}, {'_id': 0}))
    if len(result) == 0:
        response = jsonify({
            'status_code': 400,
            'message':'Contacto no encontrado'
        })
    else:
        response = jsonify({
            'status_code': 200,
            'data': result,
            'message':'Se encontró el contacto'
        })
    client.close()
    return response

app.run(debug=True, host='localhost', port=5000)