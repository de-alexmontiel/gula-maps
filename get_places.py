import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Función para obtener detalles del lugar
def obtener_detalles_lugar(place_id, api_key):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={api_key}'
    response = requests.get(url)
    json_data = response.json()
    return json_data['result']

# Función para obtener place_ids existentes en Google Sheets
def obtener_place_ids_existentes(sheet):
    records = sheet.get_all_records()
    existing_place_ids = [row['Place ID'] for row in records]
    return set(existing_place_ids)

# Función para obtener establecimientos y guardarlos en Google Sheets
def obtener_establecimientos(latlon, radius, api_key, sheet):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlon}&radius={radius}&type=cafe&key={api_key}'
    response = requests.get(url)
    json_data = response.json()
    results = json_data['results']
    todo = []

    # Obtener place_ids existentes para evitar duplicados
    existing_place_ids = obtener_place_ids_existentes(sheet)

    # Headers para las columnas
    headers = ['Place ID', 'Nombre', 'Cercanía', 'Dirección', 'Latitud', 'Longitud', 'Rating', 'Abierto Ahora', 'Tipos', 'Nivel de Precios', 'Estado del Negocio', 'Teléfono', 'URL del Lugar']
    
    # Añadir encabezados solo si no están
    if len(sheet.get_all_records()) == 0:
        sheet.append_row(headers)
    
    for result in results:
        place_id = result['place_id']

        # Validar si el place_id ya existe para evitar duplicados
        if place_id in existing_place_ids:
            continue  # Saltar si ya existe

        details = obtener_detalles_lugar(place_id, api_key)
        name = result['name']
        vicinity = result.get('vicinity', 'No disponible')
        formatted_address = result.get('formatted_address', 'No disponible')
        location = result['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        rating = result.get('rating', 0)
        opening_hours = result.get('opening_hours', {}).get('open_now', 'No disponible')
        types = ", ".join(result.get('types', []))
        price_level = result.get('price_level', 'No disponible')
        business_status = result.get('business_status', 'No disponible')
        phone = details.get('formatted_phone_number', 'No disponible')
        
        # URL del lugar en Google Maps
        place_url = f'https://www.google.com/maps/search/?api=1&query={name.replace(" ", "+")}'
        
        # Añadir fila de resultados a la lista
        todo.append([place_id, name, vicinity, formatted_address, lat, lng, rating, opening_hours, types, price_level, business_status, phone, place_url])

    # Escribir los datos en Google Sheets
    for row in todo:
        sheet.append_row(row)

    # Manejar paginación si existe un token de página siguiente
    if 'next_page_token' in json_data:
        time.sleep(2)  # Esperar para que el token sea válido
        next_url = f"{url}&pagetoken={json_data['next_page_token']}"
        obtener_establecimientos(latlon, radius, api_key, sheet)

# Autenticación con Google Sheets
def conectar_google_sheets(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Alejandro P Montiel/Super_menu_paraiso/my_project/credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

# Función principal para iniciar el script
def main():
    api_key = 'AIzaSyCBJFNQ18_xSW-SwNdywldYZC4Ck0W1FyA'  # Reemplaza con tu clave de API de Google
    latlon = '18.4062841,-93.2183717'  # Coordenadas Ciudad, Ejemplo: Paraiso Tabasco
    radius = 10000  # Radio de búsqueda en metros
    sheet_name = 'Establecimientos'  # Nombre de tu hoja de Google Sheets

    # Conectar con Google Sheets
    sheet = conectar_google_sheets(sheet_name)

    # Obtener establecimientos y guardarlos en Google Sheets
    obtener_establecimientos(latlon, radius, api_key, sheet)

if __name__ == '__main__':
    main()
