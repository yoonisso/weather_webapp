import requests
from io import BytesIO
from helpers.file_extractor import FileExtractor
from collections import defaultdict
from helpers.haversine_calculator import HarversineCalculator
from collections import defaultdict

def load_all_stations():
    """
    Loads all stations from soecified URL + load inventory of stations
     
    Returns:
        Returns list of coords, id, name and distance 

    """
    file_url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'
    inventory_url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt'
    try:

        #Inventory
        response_inventory = requests.get(inventory_url)
        response_inventory.raise_for_status()
        inventory_content_lines = response_inventory.text.split('\n')
        
        inventory = {}

        for line in inventory_content_lines:
            if(line[31:36].strip() == 'TMIN' or line[31:36].strip() == 'TMAX'):
                station_id = line[0:11]
                first_year = line[36:40]
                last_year = line[41:45]
                inventory[station_id] = [first_year,last_year]  

        #Stations
        response_stations = requests.get(file_url)
        response_stations.raise_for_status()

        # Dateiinhalt als Liste von Zeilen erhalten
        stations_content_lines = response_stations.text.split('\n')
        all_coords = []
        for line in stations_content_lines:
            if line[12:20].strip() == '' or line[21:30].strip() == '':
                continue
            else:
                
                lat = float(line[12:20].strip())
                lon = float(line[21:30].strip())
                stid = line[:11]
                city = line[41:71].strip()

                if(stid in inventory.keys()):
                    first_year = inventory[stid][0]
                    last_year = inventory[stid][1]
                else:
                    first_year = 0
                    last_year = 0
                
                coords = {'id': stid, 'city': city, 'latitude': lat, 'longitude': lon, 'first_year': first_year, 'last_year': last_year}

                all_coords.append(coords)

        return all_coords

    except requests.exceptions.RequestException as e:
        print(f'Fehler bei der Anfrage: {e}')

def get_stations_by_coordinates(all_stations, latitude, longitude, radius, station_count):
    """
    Sorts the stations by distance
    
    Args:
        all_stations (list of stations): all available stations (id, city, latitude, longitude, first_year, last_year)
        latitude (float): latitude of search point
        longitude (float): longitude of search point
        radius (int): Radius around latitude and longitude to be searched for stations
        station_count (int): count of stations to be selected
    
    Returns:
        closest stations (count: station_count)
    """

    filtered_coords = []

    for station in all_stations:
        distance = HarversineCalculator.haversine(latitude, longitude, station['latitude'], station['longitude'])
        if distance <= radius:
            station['distance'] = round(distance,2)
            filtered_coords.append(station)

    filtered_coords.sort(key=lambda a: a['distance'])

    if len(filtered_coords) < station_count:
        return filtered_coords
    else:
        return filtered_coords[0:station_count]

def get_weather_data_of_station_by_station_id(station_id):
    """
    Gets weather data of a station from Daily Global Historical Climatology Network
    Args:
        station_id (string): ID of station to be called
    Returns:
        defaultdict with data of every available year
    """

    url = f"https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/{station_id}.csv.gz"
    response = requests.get((url), stream=True)

    if response.status_code == 200:
        compressed_StationWeatherData = BytesIO(response.content)

    stationTemperatures = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    stationWeatherData = FileExtractor.extract_file(compressed_StationWeatherData)

    for record in stationWeatherData:
        year = int(record[1][0:4])
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
    print(get_weather_data_of_station_by_station_id("GME00122614"))


  





