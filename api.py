from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

def open_mongo_db():
    try:
        client = MongoClient('mongodb+srv://mverad:mverad@cluster0.uavhcn6.mongodb.net/')
        db = client['Agenda']
        coll = db['Agenda']
    except Exception as e:
        print(f'Error: {e}')
    

def look_up_contact(coll):
    """ Function returns the result of looking up for a contact by name"""
    name = input('\nNombre o Apellido: ')
    regex_pattern = f'.*{re.escape(name)}.*'
    result = list(coll.find({'nombre': {'$regex': regex_pattern, '$options': 'i'}}, {'_id': 0}))
    if len(result) == 0:
        return "Contacto no encontrado"
    else:
        return result