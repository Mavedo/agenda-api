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

@app.route('/agregar', methods=['POST'])
def new_contact():
    """We integrate all the information of the users input and add it to the MongoDB"""
    coll, client = open_mongo_db()
    name = request.args.get('nombre', type=str)
    last_name = request.args.get('apellidos', type=str)
    num = request.args.get('numero', type=int)
    email = request.args.get('email', type=str)
    number_val = number_validation(num)
    email_val = email_validation(email)

    if not number_val:
        response = jsonify({
            'status_code':400,
            'message':'El número telefónico debe constar de 10 dígitos'
        })

    elif not email_val:
        response = jsonify({
            'status_code':400,
            'message':'El formato del email no es válido'
        })

    elif name and last_name and number_val and email_val: 
        new_contact = {'nombre': name + " " + last_name,
                        'numero': num,
                        'email': email}
        coll.insert_one(new_contact)
        new_contact.pop('_id', None)
        response = jsonify({
            'status_code': 200,
            'contacto': new_contact,
            'message': 'Se añadió correctamente el contacto'
            })
    else:
        response = jsonify({
            'status_code':400,
            'message':'No se añadió el contacto. Revisar los datos'
        })
    client.close()     
    return response

def number_validation(num):
    return len(str(num)) == 10

def email_validation(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email))

@app.route('/nombres', methods=['GET'])
def print_all_names(coll):
    coll, client = open_mongo_db()
    agenda = list(coll.find({},{'_id':0}))
    if len(agenda) == 0:
        response = jsonify({
        'status_code' : 400,
        'message': 'No se encontraron contactos en la lista'
    })
    else:
        names_list = [agenda[i]['nombre'] for i in range(len(agenda))]
        response = jsonify({
        'status_code' : 200,
        'contacts': names_list,
        'message': 'No se encontraron contactos en la lista'
    })
    client.close()
    return response


app.run(debug=True, host='localhost', port=5000)