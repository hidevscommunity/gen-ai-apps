import requests
import os

def main():
    # URL del sitio web
    url = 'https://www.cboe.com/delayed_quotes/spx/quote_table'

    # Realizar la solicitud GET al sitio web
    response = requests.get(url)

    # Obtener el nombre del archivo
    filename = response.headers['Content-Disposition'].split('=')[1]

    # Ruta de destino para guardar el archivo
    destination_path = r'C:\Users\jmmar\Desktop\Dashboard-Trader\Operativa\processed'

    # Guardar el archivo en la ruta de destino
    with open(os.path.join(destination_path, filename), 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":
    main()
