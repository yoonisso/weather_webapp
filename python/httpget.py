import requests
import time

# Such Algorithmus unter verwendung eines HTTP Get Aufrufs
def search_and_print_line(url, search_string):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Dateiinhalt als Liste von Zeilen erhalten
        file_content_lines = response.text.split('\n')

        # Nach dem Suchstring in den Zeilen suchen
        matching_lines = [line for line in file_content_lines if search_string in line]

        # Gefundene Zeilen ausgeben
        for line in matching_lines:

            print(line)

    except requests.exceptions.RequestException as e:
        print(f'Fehler bei der Anfrage: {e}')

start = time.time()
# URL zur Datei und Suchstring definieren
file_url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'
search_string = 'FREIBURG'

# Nach dem Suchstring in der Datei suchen und gefundene Zeilen ausgeben
search_and_print_line(file_url, search_string)
end = time.time()


print(f"Dauer der Abfrage: {end - start}")

