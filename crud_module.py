from pymongo import MongoClient
import pandas as pd
import re #for regex


#Create new agenda entry
def new_contact(coll):
  """We integrate all the information of the users input and add it to the MongoDB"""
  name = get_name()
  num = get_phone_number()
  email = get_email()
  new_contact = {'nombre': name,
                 'numero': num,
                 'email': email}
  coll.insert_one(new_contact)
  return new_contact

def get_phone_number():
  """ This function checks if the provided number is an integer, non-negative and contains only numbers."""
  while True:
    num = (input('Provea el número telefónico de 10 dígitos: '))
    msg = 'El dato a insertar tiene que estar compuesto de números, 10 dígitos, no debe contener otros signos.'
    try:
        num = int(num)
    except ValueError as ve:
        print(msg)
        continue
    if len(str(num)) != 10 or num < 0:
      print(msg)
      continue
    else:
      break
  return num

def get_name():
  """This fuction gets the first and last(s) name(s) of the user"""
  first_name = name_input_validation('Qué nombre o nombres desea agregar?: ')
  last_name = name_input_validation('Qué apellido o apellidos desea agregar?: ')
  full_name = first_name + ' ' + last_name
  return full_name

def name_input_validation(msg):
  """This fuction validates the input with the user, before proceeding"""
  while True:
    name = input(msg)
    correct = input(f'Si {name} es correcto teclea 1, presiona cualquier otra tecla para corregir: ')
    if correct == str(1):
      break
    else:
      continue
  return name

def get_email():
  """"Receive the email input and verify if it's a valid entry """
  email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
  while True:
    email = input('Ingresa dirreción valida de correo electrónico: ')
    result = bool(re.match(email_regex,email))
    if result == True:
      break
    else:
      print('Dirección de correo inválida')
      continue
  return email

def look_up_contact(coll):
  """ Function returns the result of looking up for a contact by name"""
  name = input('\nNombre o Apellido: ')
  regex_pattern = f'.*{re.escape(name)}.*'
  result = list(coll.find({'nombre': {'$regex': regex_pattern, '$options': 'i'}}, {'_id': 0}))
  if len(result) == 0:
    return "Contacto no encontrado"
  else:
    return result
  
def delete_update_main(coll, func):
  """Function allows to search for a contact to have it's full name to either update it or delete it.
  It takes delete_contact or update_contact to complete the desired action.
  """

  while True:
    print("\nPara realizar esta acción requieres el nombre completo, tal y como está en la agenda.")
    get_contact = input("Escribe 'y' si quieres buscar un contacto o 'n' si ya tienes el nombre completo: ")
    if get_contact == 'y':
      look_up_result = look_up_contact(coll)
      print(f'\n{look_up_result}\n')
    elif get_contact == 'n':
      update_delete_result = func(coll) #we must add the correct function when running it
      return update_delete_result
    else:
      print('Entrada inválida. Por favor, escribe "y" o "n".')

def delete_contact(coll):
  """Función que se agrega a delete_update_main para completar la acción de borrar contacto."""
  name = input('\nEscribe el nombre del contacto a eliminar de la agenda: ')
  delete_it = coll.find_one_and_delete({'nombre': name}, projection={'_id': False})
  if delete_it:
    print('Contacto eliminado exitosamente')
    return delete_it
  else:
    return 'Contacto no eliminado o no encontrado'

def update_contact(coll):
  """Función que se agrega a delete_update_main para completar la acción de actualizar un contacto."""
  name = input('\nEscribe el nombre del contacto a actualizar: ')
  field_choice = input('Si quieres actualizar el nombre escribe 1, el teléfono escribe 2, el email escribe 3: ')
  options = ['1','2','3']
  if field_choice in options:
    if field_choice == str(1):
      print('Primero ingresa nombre(s), después te pediremos los apellidos.')
      new_value = {'$set': {'nombre': get_name()}}
    elif field_choice == str(2):
      new_value = {'$set': {'numero': get_phone_number()}}
    elif field_choice == str(3):
      new_value = {'$set': {'email': get_email}}
    result = coll.update_one({'nombre': name}, new_value)
    if result.modified_count > 0:
      return 'Contacto actualizado exitosamente.'
    else:
      return 'No se encontró el contacto o no se realizaron cambios.'
  else:
    print('Opción inválida. Por favor, selecciona 1, 2 o 3.')

def print_all_agenda(coll):
  """"Print all documents in the collection"""
  agenda = coll.find({},{'_id': 0})
  for contact in agenda:
    print(contact)

def menu_display():
  try:
    client = MongoClient('mongodb+srv://mverad:mverad@cluster0.uavhcn6.mongodb.net/')
    db = client['Agenda']
    coll = db['Agenda']
    while True:
      options = ['1','2','3','4','5','6']
      print('\nMenú de opciones:\n1. Crear contacto nuevo\n2. Buscar contacto\n3. Actualizar contacto\n4. Borrar contacto\n5. Ver toda la agenda\n6. Salir')
      user_choice = input('\nElija la opción deseada: ')
      if user_choice in options:
        if user_choice == '1':
          new_contact(coll)
        elif user_choice == '2':
          result = look_up_contact(coll)
          print(result)
        elif user_choice == '3':
          delete_update_main(coll, update_contact)
        elif user_choice == '4':
          delete_update_main(coll, delete_contact)
        elif user_choice == '5':
          print_all_agenda(coll)
        elif user_choice == '6':
          print('Agenda cerrada.')
          break
        else:
          print('Ingrese una opción válida.')
          continue
  except Exception as e:
    print(f'Error: {e}')
  finally:
    client.close()

menu_display()