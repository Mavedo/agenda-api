from flask import Flask, jsonify, request
from pymongo import MongoClient
import re

app = Flask(__name__)

#Create database connection so it can be cosed after each query/action
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

#Read
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

#Create contact
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

#Read
@app.route('/nombres', methods=['GET'])
def print_all_names(coll):
    """ Está función se utiliza con el método GET, para retornar todos los nombres
    de la base de datos. Solo los nombres."""
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

def update_contact():
    coll, client = open_mongo_db()
    name = request.args.get('nombre',type=str)
    name_validation = name_in_agenda(name, coll)
    value_to_update = request.args.get('dato',type=str).lower()
    new_value = request.args.get('nuevo')
    
    if not name_validation:
        response = jsonify({
            "status_code":400,
            "message":"Nombre del contacto no se encontró en la agenda"
        })
    if (value_to_update == 'numero' or 'telefono'):
        if not number_validation(new_value):
            response = jsonify({
                "status_code":400,
                "message": "El número de teléfono debe constar de 10 dígitos"
            })
        else:
            coll.update_one({'nombre':name}, {'$set': {'numero': new_value}})
            response = jsonify({
                'status_code':200,
                'message': f''
            })
        pass
    elif (value_to_update == 'email' or 'mail'):
        if not email_validation(new_value):
            response = jsonify({
                "status_code": 400,
                "message":f"{new_value} no cumple con el formato de correo electrónico"
            })

def name_in_agenda(name, coll):
    return coll.find_one({'nombre': {'$regex': f'^{re.escape(name)}$', '$options': 'i'}}) is not None

app.run(debug=True, host='localhost', port=5000)