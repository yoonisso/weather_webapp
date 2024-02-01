import requests
import time
from math import radians, sin, cos, sqrt, atan2


# Such Algorithmus unter verwendung eines HTTP Get Aufrufs
def search_and_print_line(url, target_coords, radius):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Dateiinhalt als Liste von Zeilen erhalten
        file_content_lines = response.text.split('\n')
        all_coords = []
        for line in file_content_lines:
            if line[12:20].strip() == '' or line[21:30].strip() == '':
                continue
            else:
                lat = float(line[12:20].strip())
                lon = float(line[21:30].strip())
                stid = line[:11]
                coords = (lat, lon, stid)

                all_coords.append(coords)

        #print(all_coords)
        filtered_coords = []

        for coords in all_coords:
            distance = haversine(target_coords[0], target_coords[1], coords[0], coords[1])
            if distance <= radius:
                filtered_coords.append(coords)

        return filtered_coords

    except requests.exceptions.RequestException as e:
        print(f'Fehler bei der Anfrage: {e}')


def haversine(lat1, lon1, lat2, lon2):
    # Radius der Erde in Kilometern
    R = 6371.0

    # Umrechnung der Breiten- und Längengrade von Grad in Radian
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Deltas der Breiten- und Längengrade
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine-Formel
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Entfernung berechnen
    distance = R * c

    return distance


start = time.time()
# URL zur Datei und Suchstring definieren
file_url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'

# Zielkoordinaten und Radius
target_coords = (48.06009192096103, 8.533905572877782)
radius = 50  # in Kilometern

# Nach dem Suchstring in der Datei suchen und gefundene Zeilen ausgeben
print(f"Gefunde Koordinaten, IDs: {search_and_print_line(file_url, target_coords, radius)}")

end = time.time()

print("")
print(f"Dauer der Abfrage: {end - start}")

