from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Función para conectar a Google Sheets y obtener datos
def obtener_datos_google_sheets():
    # Autenticación y conexión con Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Alejandro P Montiel/Super_menu_paraiso/my_project/credentials.json', scope)
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

    # Filtrar solo los registros con 'Estado del Negocio' igual a 'OPERATIONAL'
    filtered_data = [row for row in data if row.get('Estado del Negocio') == 'OPERATIONAL']

    # Separar los datos por tipo (restaurantes, bares, cafeterías)
    restaurants = [row for row in filtered_data if 'Restaurant' in row['Tipos']]
    bars = [row for row in filtered_data if 'Bar' in row['Tipos']]
    cafes = [row for row in filtered_data if 'Cafe' in row['Tipos']]
    
    # Renderizar la página con los datos filtrados
    return render_template('index.html', restaurants=restaurants, bars=bars, cafes=cafes)

if __name__ == '__main__':
    app.run(debug=True)
