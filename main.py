import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Słownik zawierający identyfikatory województw w bazie GUS
WOJEWODZTWA = {
    "POLSKA": 33617,
    "MAŁOPOLSKIE": 33619,
    "ŚLĄSKIE": 33929,
    "LUBUSKIE": 34187,
    "WIELKOPOLSKIE": 34353,
    "ZACHODNIOPOMORSKIE": 34815,
    "DOLNOŚLĄSKIE": 35067,
    "OPOLSKIE": 35390,
    "KUJAWSKO-POMORSKIE": 35542,
    "POMORSKIE": 35786,
    "WARMIŃSKO-MAZURSKIE": 35976,
    "ŁÓDZKIE": 36185,
    "ŚWIĘTOKRZYSKIE": 36450,
    "LUBELSKIE": 36627,
    "PODKARPACKIE": 36924,
    "PODLASKIE": 37185,
    "MAZOWIECKIE": 37380
}

# Słownik zawierający identyfikatory działów budżetowych w bazie GUS
DZIALY = {
    "Transport i łączność": 7350010,
    "Turystyka": 7350022,
    "Gospodarka mieszkaniowa": 7350032,
    "Administracja publiczna": 7350235,
    "Rolnictwo i łowiectwo": 7361254,
    "Oświata i wychowanie": 7361382,
    "Ochrona zdrowia": 7361393,
    "Pomoc społeczna": 7361400,
    "Edukacyjna opieka wychowawcza": 7361442,
    "Rodzina": 7361444,
    "Gospodarka komunalna": 7361445,
    "Kultura": 7361450,
    "Kultura fizyczna": 7361480,
    "Ogółem": 7361493
}

def get_gus_income_data(year, wojewodztwo_id, dzial_id):
    """
    Pobiera dane z API GUS dla określonego roku, województwa i działu
    Zwraca odpowiedź w formacie JSON
    """
    base_url = "https://api-dbw.stat.gov.pl/api/1.1.0/variable/variable-data-section"
    params = {
        "id-zmienna": "1192",  # ID zmiennej dla dochodów
        "id-przekroj": "1046", # ID przekroju danych
        "id-rok": str(year),
        "id-okres": "282",     # Okres roczny
        "ile-na-stronie": "5000",
        "numer-strony": "0",
        "lang": "pl"
    }
    
    response = requests.get(base_url, params=params)
    return response.json()

def create_earnings_chart(wojewodztwo_nazwa, dzial_nazwa):
    """
    Tworzy wykres i plik CSV z danymi o dochodach dla wybranego województwa i działu
    Zapisuje wykres jako PNG i dane jako CSV
    Zwraca DataFrame z zebranymi danymi
    """
    wojewodztwo_id = WOJEWODZTWA[wojewodztwo_nazwa]
    dzial_id = DZIALY[dzial_nazwa]
    
    years = range(2010, 2023)  # Zakres lat 2010-2022
    earnings = []
    
    # Pobieranie danych dla każdego roku
    for year in years:
        data = get_gus_income_data(year, wojewodztwo_id, dzial_id)
        for item in data['data']:
            if item['id-pozycja-1'] == wojewodztwo_id and item['id-pozycja-2'] == dzial_id:
                earnings.append(item['wartosc'])
                break
    
    # Tworzenie wykresu
    plt.figure(figsize=(12, 6))
    plt.plot(list(years), earnings, marker='o')
    plt.title(f'Dochody dla {wojewodztwo_nazwa} - {dzial_nazwa} (2010-2022)')
    plt.xlabel('Rok')
    plt.ylabel('Wartość (PLN)')
    plt.grid(True)
    
    # Generowanie nazwy pliku z aktualną datą
    filename = f'dochody_{wojewodztwo_nazwa}_{dzial_nazwa}_{datetime.now().strftime("%Y%m%d")}'
    plt.savefig(f'{filename}.png')
    
    # Zapisywanie danych do CSV
    df = pd.DataFrame({
        'rok': list(years),
        'dochody': earnings
    })
    df.to_csv(f'{filename}.csv', index=False)
    
    return df

def main():
    """
    Główna funkcja programu:
    1. Wyświetla dostępne województwa
    2. Pobiera wybór użytkownika
    3. Wyświetla dostępne działy
    4. Pobiera wybór użytkownika
    5. Generuje i zapisuje wykres oraz dane
    """
    print("Dostępne województwa:")
    for i, woj in enumerate(WOJEWODZTWA.keys(), 1):
        print(f"{i}. {woj}")
    
    woj_choice = int(input("\nWybierz numer województwa: ")) - 1
    wojewodztwo = list(WOJEWODZTWA.keys())[woj_choice]
    
    print("\nDostępne działy:")
    for i, dzial in enumerate(DZIALY.keys(), 1):
        print(f"{i}. {dzial}")
    
    dzial_choice = int(input("\nWybierz numer działu: ")) - 1
    dzial = list(DZIALY.keys())[dzial_choice]
    
    print(f"\nGenerowanie wykresu dla {wojewodztwo} - {dzial}")
    df = create_earnings_chart(wojewodztwo, dzial)
    print("\nZebrane dane:")
    print(df)
    print("\nWykres został zapisany jako PNG")

if __name__ == "__main__":
    main()
