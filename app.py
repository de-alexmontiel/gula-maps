from flask import Flask, render_template, request, make_response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv  # Importar la librería

# Cargar variables de entorno desde el archivo .env
load_dotenv()  # Esto cargará automáticamente el archivo .env

app = Flask(__name__)

# Función para conectar a Google Sheets y obtener datos
def obtener_datos_google_sheets():
    # Autenticación y conexión con Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Obtener las credenciales desde la variable de entorno
    google_creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Convertir el JSON de la variable de entorno en un diccionario
    creds_dict = json.loads(google_creds_json)

    # Usar las credenciales del diccionario para autenticar
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # Abrir la hoja de cálculo y seleccionar la pestaña 'Establecimientos'
    sheet = client.open('Establecimientos').worksheet('Establecimientos')
    
    # Obtener todos los registros de la hoja
    data = sheet.get_all_records()
    
    # Retornar todos los datos para luego filtrarlos en la vista
    return data

@app.route('/')
def index():
    # Obtener todos los datos de Google Sheets
    data = obtener_datos_google_sheets()

    # Obtener la ciudad seleccionada del parámetro de consulta o la cookie, si no, usar 'Paraíso' por defecto
    selected_city = request.args.get('ciudad', request.cookies.get('ciudad', 'Paraíso'))

    # Obtener el término de búsqueda de palabra clave o tipo de comida
    search_query = request.args.get('search', '').lower()  # Convertir a minúsculas para búsqueda insensible a mayúsculas

    # Filtrar solo los registros con 'Estado del Negocio' igual a 'OPERATIONAL'
    filtered_data = [row for row in data if row.get('Estado del Negocio') == 'OPERATIONAL']

    # Filtrar por ciudad seleccionada
    filtered_data = [row for row in filtered_data if row.get('Ciudad') == selected_city]

    # Filtrar por palabras clave si existe una búsqueda
    if search_query:
        filtered_data = [
            row for row in filtered_data 
            if search_query in row.get('Tipos', '').lower() or search_query in row.get('Palabras_Clave', '').lower() or search_query in row.get('Tipo_comida', '').lower()
        ]

    # Separar los datos por tipo (restaurantes, bares, cafeterías)
    restaurants = [row for row in filtered_data if 'Restaurant' in row['Tipos']]
    bars = [row for row in filtered_data if 'Bar' in row['Tipos']]
    cafes = [row for row in filtered_data if 'Cafe' in row['Tipos']]
    
    # Obtener la lista de ciudades para el filtro
    ciudades = sorted(list(set(row['Ciudad'] for row in data)))

    # Crear una respuesta para permitir el almacenamiento de la ciudad seleccionada en cookies
    response = make_response(render_template('index.html', restaurants=restaurants, bars=bars, cafes=cafes, ciudades=ciudades, selected_city=selected_city))

    # Si la ciudad seleccionada no está en las cookies, guardarla
    if 'ciudad' not in request.cookies or request.cookies.get('ciudad') != selected_city:
        response.set_cookie('ciudad', selected_city)
    
    return response


if __name__ == '__main__':
    app.run(debug=True)
