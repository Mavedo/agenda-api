# My API

Welcome to the documentation for My API. This API allows you to manage contacts in an agenda allocated in mongoDB.

## Getting Started

To get started with the API, you'll need to install Python, Flask and Pymongo. Then, you can clone the repository and install the dependencies.

### Endpoints:


'GET /buscar':

Parameter: 'nombre'
- The name is case insensitive, bust if there are special characters in the names such as accents, they must be typed.
- It returns all the contacts in the agenda that matches the provided name.

example: '/buscar?nombre=martín'


'GET /nombres':

- Returns all names for the contacts in the agenda
- Receives no parameters


'POST /agregar':

Parameters: nombre, apellidos, numero, email.

nombre: May receive one or more names. Will be joint with 'apellidos'.
apellidos: May receive one or more names. Will be joint with 'nombre' to the 'nombre' key.
numero: It takes a phone number composed of 10 digits.
email: Receives an email address under the classic format of username@site.com

-It adds the contact to the agenda if they provided parameters fullfil with the criteria.

example: '/agregar?nombre=Jesús Alfredo&apellido=Ramírez Estrada&numero=1234567890&email=jesusalfredo@mail.com'


'PUT /actualizar'

Parameters: nombre, dato, nuevo.

nombre: It must be passed as it is written in the agenda, all words must be present (name and last name).
dato: It receives the category that is desired for updating: nombre, numero or email.
nuevo: The new value for the provided category is passed for updating.

-It updates a category from a contact in the agenda, the contact must be in the agenda and the name must be passed as it is present

example: '/actualizar?nombre=Jesús Alfredo Ramírez Estrada&dato=email&nuevo=nuevocorreo@mail.com'


'DELETE /eliminar'

Parameters: nombre

nombre: It must be passed as it is written in the agenda, all words must be present (name and last name).

-Deletes a contact from the agenda, the name must be provided as it's written in the agenda.

example: '/eliminar?nombre=Jesús Alfredo Ramírez Estrada'