import requests
from io import BytesIO
from helpers.file_extractor import FileExtractor
from collections import defaultdict
from helpers.haversine_calculator import HarversineCalculator

def load_all_stations():
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

def get_stations_by_coordinates(allStations, latitude, longitude, radius, stationCount):
    """
    Sorts the stations by distance and returns the closest ones (stationCount)
    
    """

    filtered_coords = []

    for station in allStations:
        distance = HarversineCalculator.haversine(latitude, longitude, station['latitude'], station['longitude'])
        if distance <= radius:
            station['distance'] = round(distance,2)
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

def get_weather_data_of_station_by_station_id(stationId, startYear, endYear):
    url = f"https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/{stationId}.csv.gz"
    response = requests.get((url), stream=True)

    if response.status_code == 200:
        compressed_StationWeatherData = BytesIO(response.content)

    stationTemperatures = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    stationWeatherData = FileExtractor.extract_file(compressed_StationWeatherData)

    for record in stationWeatherData:
        year = int(record[1][0:4])
        if year < startYear or year > endYear:
            continue
        month = record[1][4:6]
        if month[0] == '0':
            month = int(month[1])
        else:
            month = int(month)
        day = record[1][6:8]
        if day[0] == '0':
            day = int(day[1])
        else:
            day = int(day)
        if record[2] == 'TMIN':
                temperature = float(record[3]) / 10
                stationTemperatures[year][month][day]['TMIN'] = temperature
        elif record[2] == 'TMAX':
                temperature = float(record[3]) / 10
                stationTemperatures[year][month][day]['TMAX'] = temperature        

    return stationTemperatures
    

#Currently testing getWeatherDataOfStationByStationId-Method
if __name__ == "__main__":
    print(get_weather_data_of_station_by_station_id("GME00122614", 1949, 1951))


  





