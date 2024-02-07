from bokeh.plotting import figure
from bokeh.embed import components

#Testdata yearly
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

#Testdata monthly
averageTemperaturesMonthly = {
    1: {'TMIN': 4.3, 'TMAX': 14.7},
    2: {'TMIN': 5.1, 'TMAX': 15.2},
    3: {'TMIN': 3.8, 'TMAX': 14.5},
    4: {'TMIN': 6.2, 'TMAX': 16.8},
    5: {'TMIN': 4.5, 'TMAX': 15.0},
    6: {'TMIN': 5.3, 'TMAX': 15.7},
    7: {'TMIN': 4.8, 'TMAX': 14.9},
    8: {'TMIN': 6.0, 'TMAX': 16.5},
    9: {'TMIN': 5.7, 'TMAX': 15.4},
    10: {'TMIN': 4.1, 'TMAX': 14.2},
    11: {'TMIN': 5.6, 'TMAX': 15.8},
    12: {'TMIN': 4.9, 'TMAX': 15.1}
}

def countAverageTempByDict(averageTemperatures):
    return [(data['TMAX'] + data['TMIN']) / 2 for data in averageTemperatures.values()]


class DiagramPloter:
    @staticmethod
    def plotDiagram(averageTemperatures, diagram_type, x_axis_label):

        #TODO needs to be adjusted for laptop and monitor screens
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        p = figure(sizing_mode="scale_both", min_width=min_width,
                   min_height=min_height, max_height=max_height,
                   max_width=max_width, title=diagram_type,
                   x_axis_label=x_axis_label, y_axis_label='Temperatur',
                   toolbar_location=None, tools=[])

        #TMAX plot
        p.line(
            [year for year in averageTemperatures.keys()],
            [data['TMAX'] for data in averageTemperatures.values()],
            color="red"
        )

        p.circle(
            [year for year in averageTemperatures.keys()],
            [data['TMAX'] for data in averageTemperatures.values()],
            color="red",
            size=5
        )

        #TMIN plot
        p.line(
            [year for year in averageTemperatures.keys()],
            [data['TMIN'] for data in averageTemperatures.values()],
            color="blue"
        )

        p.circle(
            [year for year in averageTemperatures.keys()],
            [data['TMIN'] for data in averageTemperatures.values()],
            color="blue",
            size=5
        )

        #TAVG plot
        average_temperatures= countAverageTempByDict(averageTemperatures)

        p.line(
            [year for year in averageTemperatures.keys()],
            average_temperatures,
            color="green",
            line_dash='dashed'
        )

        p.circle(
            [year for year in averageTemperatures.keys()],
            average_temperatures,
            color="green",
            size=5
        )
        script, div = components(p)

        return script, div


if(__name__ == "__main__"):
    #Testing only
    DiagramPloter.plotDiagram(averageTemperaturesYear, "Jahresansicht", "Jahre")