import requests
from math import radians, sin, cos, sqrt, atan2

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


def loadAllStations():
    """
    Loads all stations from given URL. Result is list of coords and id 

    """
    file_url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'
    try:
        response = requests.get(file_url)
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
                city = line[41:71].strip()
                
                coords = {'id': stid, 'city': city, 'latitude': lat, 'longitude': lon}

                all_coords.append(coords)

        return all_coords

    except requests.exceptions.RequestException as e:
        print(f'Fehler bei der Anfrage: {e}')

def getStationsByCoordinates(allStations, latitude, longitude, radius, stationCount):
    """
    Sorts the stations by distance and returns the closest ones (stationCount)
    
    """

    filtered_coords = []

    for station in allStations:
        distance = haversine(latitude, longitude, station['latitude'], station['longitude'])
        if distance <= radius:
            # coords = (station['id'], station['city'],station['latitude'],station['longitude'], distance) #Siehe oben coords + distance
            # coords = {'id': stid, 'city': city, 'latitude': lat, 'longitude': lon, 'distance': distance}
            station['distance'] = distance
            filtered_coords.append(station)

    # #Testdaten
    # filtered_coords = [(49.5042, 11.0567, 'GME00102380', 5.762299315009502),
    #                    (49.6506, 11.0083, 'GME00121882', 19.344037382016104),
    #                    (49.5703, 10.9942, 'GME00121894', 10.370968197733994),
    #                    (49.1792, 11.375, 'GME00122494', 43.369941499575)]
    filtered_coords.sort(key=lambda a: a['distance'])

    if len(filtered_coords) < stationCount:
        return filtered_coords
    else:
        return filtered_coords[0:stationCount]


  









