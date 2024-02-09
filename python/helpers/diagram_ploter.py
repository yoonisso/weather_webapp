from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, CustomJS

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

def checkIfYearOrMonthViewByDiagramType(diagram_type):
    #needs to check if year or month for TOOLTIPS
    return "Jahr"


class DiagramPloter:
    #TODO create Legend
    #TODO fix hovereffect, add time of year to hover
    @staticmethod
    def plotDiagram(averageTemperatures, diagram_type, x_axis_label, chosen_views):
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        year_tmin_color = "blue"
        year_tmax_color = "red"

        spring_tmin_color = "#90ee90"
        spring_tmax_color = "#006400"

        summer_tmin_color = "#add8e6"
        summer_tmax_color = "#00008b"

        fall_tmin_color = "#ffa500"
        fall_tmax_color = "#ff8c00"

        winter_tmin_color = "#d3d3d3"
        winter_tmax_color = "#696969"

        #Hover Effect
        TOOLTIPS = [
            ("Jahr", "@x"),
            ("Temperatur", "@y")
        ]

        p = figure(sizing_mode="scale_both", min_width=min_width,
                   min_height=min_height, max_height=max_height,
                   max_width=max_width, title=diagram_type,
                   x_axis_label=x_axis_label, y_axis_label='Temperatur',
                   toolbar_location=None, tools=[])

        hover = HoverTool(tooltips=TOOLTIPS)

        p.add_tools(hover)

        #year TMAX plot
        if chosen_views['year']['TMAX']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMAX'] for data in averageTemperatures.values()],
                color=year_tmax_color,
                line_width=3
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMAX'] for data in averageTemperatures.values()],
                color=year_tmax_color,
                size=10
            )

        #year TMIN plot
        if chosen_views['year']['TMIN']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMIN'] for data in averageTemperatures.values()],
                color=year_tmin_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMIN'] for data in averageTemperatures.values()],
                color=year_tmin_color,
                size=10
            )

        #Spring TMIN
        if chosen_views['spring']['TMIN']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMIN'] for data in averageTemperatures.values()],
                color=spring_tmin_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMIN'] for data in averageTemperatures.values()],
                color=spring_tmin_color,
                size=10
            )


        #Spring TMAX
        if chosen_views['spring']['TMAX']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMAX'] for data in averageTemperatures.values()],
                color=spring_tmax_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMAX'] for data in averageTemperatures.values()],
                color=spring_tmax_color,
                size=10
            )

        #summer TMIN
        if chosen_views['summer']['TMIN']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMIN'] for data in averageTemperatures.values()],
                color=summer_tmin_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMIN'] for data in averageTemperatures.values()],
                color=summer_tmin_color,
                size=10
            )


        #Summer TMAX
        if chosen_views['summer']['TMAX']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMAX'] for data in averageTemperatures.values()],
                color=summer_tmax_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMAX'] for data in averageTemperatures.values()],
                color=summer_tmax_color,
                size=10
            )

        #Fall TMIN
        if chosen_views['fall']['TMIN']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMIN'] for data in averageTemperatures.values()],
                color=fall_tmin_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMIN'] for data in averageTemperatures.values()],
                color=fall_tmin_color,
                size=10
            )


        #Fall TMAX
        if chosen_views['fall']['TMAX']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMAX'] for data in averageTemperatures.values()],
                color=fall_tmax_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMAX'] for data in averageTemperatures.values()],
                color=fall_tmax_color,
                size=10
            )

        #Winter TMIN
        if chosen_views['winter']['TMIN']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMIN'] for data in averageTemperatures.values()],
                color=winter_tmin_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMIN'] for data in averageTemperatures.values()],
                color=winter_tmin_color,
                size=10
            )


        #Winter TMAX
        if chosen_views['winter']['TMAX']:
            p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMAX'] for data in averageTemperatures.values()],
                color=winter_tmax_color,
                line_width=4
            )

            p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMAX'] for data in averageTemperatures.values()],
                color=winter_tmax_color,
                size=10
            )

        script, div = components(p)

        return script, div


if(__name__ == "__main__"):
    #Testing only
    DiagramPloter.plotDiagram(averageTemperaturesYear, "Jahresansicht", "Jahre")