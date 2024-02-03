import matplotlib.pyplot as plt

#Testdata
averageTemperaturesYear = {
    1949: {'TMIN': 4.3, 'TMAX': 14.7},
    1950: {'TMIN': 5.1, 'TMAX': 15.2},
    1951: {'TMIN': 3.8, 'TMAX': 14.5},
    1952: {'TMIN': 6.2, 'TMAX': 16.8},
    1953: {'TMIN': 4.5, 'TMAX': 15.0},
    1954: {'TMIN': 5.3, 'TMAX': 15.7},
    1955: {'TMIN': 4.8, 'TMAX': 14.9},
    1956: {'TMIN': 6.0, 'TMAX': 16.5},
    1957: {'TMIN': 5.7, 'TMAX': 15.4},
    1958: {'TMIN': 4.1, 'TMAX': 14.2},
    1959: {'TMIN': 5.6, 'TMAX': 15.8},
    1960: {'TMIN': 4.9, 'TMAX': 15.1},
    1961: {'TMIN': 5.2, 'TMAX': 15.3},
    1962: {'TMIN': 4.4, 'TMAX': 14.6},
    1963: {'TMIN': 5.0, 'TMAX': 15.6},
    1964: {'TMIN': 6.1, 'TMAX': 16.2},
    1965: {'TMIN': 4.7, 'TMAX': 15.5},
    1966: {'TMIN': 5.4, 'TMAX': 15.9},
    1967: {'TMIN': 4.2, 'TMAX': 14.3},
    1968: {'TMIN': 5.5, 'TMAX': 16.0},
    # Füge hier weitere Jahre mit den entsprechenden Temperaturwerten hinzu
}

class DiagramPloter:
    def plotDiagram(averageTemperaturesYears, startYear, endYear):

        years = list(averageTemperaturesYear.keys())
        tmin_values = [data['TMIN'] for data in averageTemperaturesYear.values()]
        tmax_values = [data['TMAX'] for data in averageTemperaturesYear.values()]

        #size (can be adjusted)
        plt.figure(figsize=(10, 5))

        plt.plot(years, tmin_values, label='TMIN', marker='o')
        plt.plot(years, tmax_values, label='TMAX', marker='o')

        #Costumization
        plt.title(f'Average Temperatures from {startYear} to {endYear}')
        plt.xlabel('Year')
        plt.ylabel('Temperature')
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()

if(__name__ == "__main__"):
    DiagramPloter.plotDiagram(averageTemperaturesYear, "1949", "1968")