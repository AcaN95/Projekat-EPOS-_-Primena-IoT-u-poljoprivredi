import requests
import os
import sys
from datetime import datetime

# Unapred postavljeni API ključ
API_KEY = "dd611f339cda91b54411dc549a7b1c0a"

def clear_terminal():
    # Očisti terminal (Linux/Unix)
    # os.system('clear') 

    # Očisti terminal (Windows)
    os.system('cls')

def kelvin_to_celsius(kelvin):
    # Konverzija Kelvin u Celsius
    return kelvin - 273.15

def convert_unix_time(unix_time):
    # Konverzija UNIX vremena u formatiranu datuim-vreme
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

def get_weather_data(lat, lon, api_key):
    # Kreiranje URL-a sa parametrima
    url = f"https://api.agromonitoring.com/agro/1.0/weather?lat={lat}&lon={lon}&appid={api_key}"

    # Slanje GET zahteva
    response = requests.get(url)

    # Provera da li je zahtev uspeo (status code 200)
    if response.status_code == 200:
        # Prikaz rezultata
        weather_data = response.json()
        temperature_celsius = kelvin_to_celsius(weather_data['main']['temp'])
        formatted_time = convert_unix_time(weather_data['dt'])
        print("Vremenski podaci:")
        print(f"Vreme: {formatted_time}")
        print(f"Temperatura: {temperature_celsius:.2f} °C")
        print(f"Opis vremena: {weather_data['weather'][0]['description']}")
        print(f"Brzina vetra: {weather_data['wind']['speed']} m/s")
    else:
        print(f"Greška u zahtevu. Status code: {response.status_code}")

def get_weather_forecast(lat, lon, api_key):
    # Kreiranje URL-a za dobijanje vremenske prognoze
    url = f"https://api.agromonitoring.com/agro/1.0/weather/forecast?lat={lat}&lon={lon}&appid={api_key}"

    # Slanje GET zahteva
    response = requests.get(url)

    # Provera da li je zahtev uspeo (status code 200)
    if response.status_code == 200:
        # Prikaz rezultata
        weather_forecast = response.json()
        print("Vremenska prognoza:")
        for forecast_entry in weather_forecast:
            temperature_celsius = kelvin_to_celsius(forecast_entry['main']['temp'])
            formatted_time = convert_unix_time(forecast_entry['dt'])
            print(f"Vreme: {formatted_time}, Temperatura: {temperature_celsius:.2f} °C, Opis: {forecast_entry['weather'][0]['description']}")
    else:
        print(f"Greška u zahtevu. Status code: {response.status_code}")

def get_uv_index(poly_id, api_key):
    # Kreiranje URL-a za dobijanje indeksa UV zračenja
    url = f"http://api.agromonitoring.com/agro/1.0/uvi?polyid={poly_id}&appid={api_key}"

    # Slanje GET zahteva
    response = requests.get(url)

    # Provera da li je zahtev uspeo (status code 200)
    if response.status_code == 200:
        # Prikaz rezultata
        uv_index_data = response.json()
        formatted_time = convert_unix_time(uv_index_data['dt'])
        print("Indeks UV zračenja:")
        print(f"Vreme: {formatted_time}, UV indeks: {uv_index_data['uvi']}")
    else:
        print(f"Greška u zahtevu. Status code: {response.status_code}")

def list_parcels(api_key):
    # Kreiranje URL-a za dobijanje podataka o poligonima
    url = f"http://api.agromonitoring.com/agro/1.0/polygons?appid={api_key}"

    # Slanje GET zahteva
    response = requests.get(url)

    # Provera da li je zahtev uspeo (status code 200)
    if response.status_code == 200:
        # Prikaz rezultata
        polygon_data_list = response.json()
        
        print("Izaberite parcelu:")
        for index, polygon_data in enumerate(polygon_data_list, start=1):
            print(f"{index}. {polygon_data['name']}")
        print(f"{len(polygon_data_list)+1}. Nazad")
        print(f"{len(polygon_data_list)+2}. Izlaz")

        # Unos korisničkog izbora
        selected_index = int(input("Unesite redni broj parcele: ")) - 1

        # Provera ispravnosti izbora
        if 0 <= selected_index < len(polygon_data_list):
            selected_polygon = polygon_data_list[selected_index]
            print(f"Izabrana parcela: {selected_polygon['name']}")
            return selected_polygon
        elif selected_index == len(polygon_data_list):
            # Korisnik želi da se vrati nazad
            return None
        elif selected_index == len(polygon_data_list) + 1:
            # Korisnik želi da završi program
            print("Izlaz iz programa.")
            sys.exit()
        else:
            print("Nevažeći izbor.")
            return None

    else:
        print(f"Greška u zahtevu. Status code: {response.status_code}")
        return None

def display_parcel_options(selected_polygon):
    # Prikazi opcije za izabranu parcelu
    while True:
        print(f"\nOpcije za parcelu {selected_polygon['name']}:")
        print("1. Prikazi vremenske podatke")
        print("2. Prikazi vremensku prognozu")
        print("3. Prikazi indeks UV zračenja")
        print("4. Ovde cu kasnije dodati nesto")
        print(f"5. Nazad")
        print(f"6. Izlaz")

        # Unos korisničkog izbora
        option_choice = input("Unesite broj opcije: ")

        # Provera korisničkog izbora
        if option_choice == "1":
            # Postavke za poziv API-ja za vremenske podatke
            latitude = selected_polygon['center'][1]
            longitude = selected_polygon['center'][0]
            clear_terminal()
            # Poziv funkcije za dobijanje vremenskih podataka
            get_weather_data(latitude, longitude, API_KEY)
        elif option_choice == "2":
            # Postavke za poziv API-ja za vremensku prognozu
            latitude = selected_polygon['center'][1]
            longitude = selected_polygon['center'][0]
            clear_terminal()
            # Poziv funkcije za dobijanje vremenske prognoze
            get_weather_forecast(latitude, longitude, API_KEY)
        elif option_choice == "3":
            # Postavke za poziv API-ja za indeks UV zračenja
            poly_id = selected_polygon['id']
            clear_terminal()
            # Poziv funkcije za dobijanje indeksa UV zračenja
            get_uv_index(poly_id, API_KEY)
        elif option_choice == "4":
            clear_terminal()
            # Dodajte logiku za četvrtu opciju
            print("Izabrana je opcija 4.")
        elif option_choice == "5":
            clear_terminal()
            # Vraćanje korak unazad
            break
        elif option_choice == "6":
            # Korisnik želi da završi program
            print("Izlaz iz programa.")
            sys.exit()
        else:
            print("Nevažeći izbor.")

if __name__ == "__main__":
    while True:
        clear_terminal()
        # Dobijanje podataka o poligonima i izbor parcele
        selected_polygon = list_parcels(API_KEY)

        if selected_polygon:
            # Prikaz opcija za izabranu parcelu
            clear_terminal()
            display_parcel_options(selected_polygon)
        else:
            # Korisnik je odabrao opciju "Nazad" ili "Izlaz"
            break
