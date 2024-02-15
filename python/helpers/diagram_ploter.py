from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, Legend, TapTool, CustomJS, OpenURL

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

class DiagramPloter:
    @staticmethod
    def plotYearDiagram(averageTemperatures, chosen_views, url):
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        year_tmin_color = "#0000FF"
        year_tmax_color = "#FF0000"

        spring_tmin_color = "#7CFC00"
        spring_tmax_color = "#9ACD32"

        summer_tmin_color = "#FFD700"
        summer_tmax_color = "#ffff00"

        fall_tmin_color = "#FFA500"
        fall_tmax_color = "#FF8C00"

        winter_tmin_color = "#D3D3D3"
        winter_tmax_color = "#B0E0E6"

        #Hover Effect
        TOOLTIPS = [
            ("Jahr", "@x"),
            ("Temperatur", "@y")
        ]

        p = figure(sizing_mode="scale_both", min_width=min_width,
                   min_height=min_height, max_height=max_height,
                   max_width=max_width, title='Jahresansicht',
                   x_axis_label="Jahr", y_axis_label='Temperatur',
                   toolbar_location=None, tools=["tap"])

        hover = HoverTool(tooltips=[("Jahr", "@x"), ("Temperatur", "@y{0.0}°C")])

        p.add_tools(hover)

        legend_items = []

        #year TMAX plot
        if chosen_views['year']['TMAX']:
            line_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMAX'] for data in averageTemperatures.values()],
                color=year_tmax_color,
                line_width=3
            )

            circle_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMAX'] for data in averageTemperatures.values()],
                color=year_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Jahr", [line_tmax, circle_tmax]))

        #year TMIN plot
        if chosen_views['year']['TMIN']:
            line_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMIN'] for data in averageTemperatures.values()],
                color=year_tmin_color,
                line_width=4
            )

            circle_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMIN'] for data in averageTemperatures.values()],
                color=year_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Jahr", [line_tmin, circle_tmin]))

        #Spring TMAX
        if chosen_views['spring']['TMAX']:
            line_spring_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMAX'] for data in averageTemperatures.values()],
                color=spring_tmax_color,
                line_width=4
            )

            circle_spring_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMAX'] for data in averageTemperatures.values()],
                color=spring_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Frühling", [line_spring_tmax, circle_spring_tmax]))

        #Spring TMIN
        if chosen_views['spring']['TMIN']:
            line_spring_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMIN'] for data in averageTemperatures.values()],
                color=spring_tmin_color,
                line_width=4
            )

            circle_spring_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMIN'] for data in averageTemperatures.values()],
                color=spring_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Frühling", [line_spring_tmin, circle_spring_tmin]))

        #Summer TMAX
        if chosen_views['summer']['TMAX']:
            line_summer_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMAX'] for data in averageTemperatures.values()],
                color=summer_tmax_color,
                line_width=4
            )

            circle_summer_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMAX'] for data in averageTemperatures.values()],
                color=summer_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Sommer", [line_summer_tmax, circle_summer_tmax]))

        #summer TMIN
        if chosen_views['summer']['TMIN']:
            line_summer_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMIN'] for data in averageTemperatures.values()],
                color=summer_tmin_color,
                line_width=4
            )

            circle_summer_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMIN'] for data in averageTemperatures.values()],
                color=summer_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Sommer", [line_summer_tmin, circle_summer_tmin]))

        #Fall TMAX
        if chosen_views['fall']['TMAX']:
            line_fall_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMAX'] for data in averageTemperatures.values()],
                color=fall_tmax_color,
                line_width=4
            )

            circle_fall_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMAX'] for data in averageTemperatures.values()],
                color=fall_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Herbst", [line_fall_tmax, circle_fall_tmax]))

        #Fall TMIN
        if chosen_views['fall']['TMIN']:
            line_fall_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMIN'] for data in averageTemperatures.values()],
                color=fall_tmin_color,
                line_width=4
            )

            circle_fall_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMIN'] for data in averageTemperatures.values()],
                color=fall_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Herbst", [line_fall_tmin, circle_fall_tmin]))

        #Winter TMAX
        if chosen_views['winter']['TMAX']:
            line_winter_tmax=p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMAX'] for data in averageTemperatures.values()],
                color=winter_tmax_color,
                line_width=4
            )

            circle_winter_tmax=p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMAX'] for data in averageTemperatures.values()],
                color=winter_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Winter", [line_winter_tmax, circle_winter_tmax]))

        #Winter TMIN
        if chosen_views['winter']['TMIN']:
            line_winter_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMIN'] for data in averageTemperatures.values()],
                color=winter_tmin_color,
                line_width=4
            )

            circle_winter_tmin= p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMIN'] for data in averageTemperatures.values()],
                color=winter_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Winter", [line_winter_tmin, circle_winter_tmin]))

        legend = Legend(items=legend_items)
        p.add_layout(legend, 'right')

        tap_callback = CustomJS(args=dict(url=url), code="""
            const selected_index = cb_data.source.selected.indices[0];
            const year = cb_data.source.data['x'][selected_index];
            
            const new_url = url + "/" + year;
            
            window.location.href = new_url;
            
            cb_data.source.selected.indices = [];
            """)

        taptool = p.select(type=TapTool)
        taptool.callback = tap_callback

        script, div = components(p)

        return script, div

    @staticmethod
    def plotMonthDiagram(averageTemperatures, show_tmin, show_tmax, url):
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        month_tmin_color = "blue"
        month_tmax_color = "red"

        #Hover Effect
        TOOLTIPS = [
            ("Monat", "@x"),
            ("Temperatur", "@y")
        ]

        p = figure(sizing_mode="scale_both", min_width=min_width,
                   min_height=min_height, max_height=max_height,
                   max_width=max_width, title='Monatsansicht',
                   x_axis_label="Monat", y_axis_label='Temperatur',
                   toolbar_location=None, tools=["tap"])

        hover = HoverTool(tooltips=[("Monat", "@x"), ("Temperatur", "@y{0.0}°C")])

        p.add_tools(hover)

        legend_items = []

        #month TMAX plot
        if show_tmax:
            line_tmax = p.line(
                x = [month for month in averageTemperatures.keys()],
                y = [data['TMAX'] for data in averageTemperatures.values()],
                color=month_tmax_color,
                line_width=3
            )

            circle_tmax = p.circle(
                x = [month for month in averageTemperatures.keys()],
                y = [data['TMAX'] for data in averageTemperatures.values()],
                color=month_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Monat", [line_tmax, circle_tmax]))

        #month TMIN plot
        if show_tmin:
            line_tmin = p.line(
                x = [month for month in averageTemperatures.keys()],
                y = [data['TMIN'] for data in averageTemperatures.values()],
                color=month_tmin_color,
                line_width=4
            )

            circle_tmin = p.circle(
                x = [month for month in averageTemperatures.keys()],
                y = [data['TMIN'] for data in averageTemperatures.values()],
                color=month_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Monat", [line_tmin, circle_tmin]))

        legend = Legend(items=legend_items)
        p.add_layout(legend, 'right')

        tap_callback = CustomJS(args=dict(url=url), code="""
            const selected_index = cb_data.source.selected.indices[0];
            const month = cb_data.source.data['x'][selected_index];
            
            const new_url = url + "/" + month;
            
            window.location.href = new_url;
            
            cb_data.source.selected.indices = [];
            """)

        taptool = p.select(type=TapTool)
        taptool.callback = tap_callback

        script, div = components(p)

        return script, div

    @staticmethod
    def plotDayDiagram(averageTemperatures, show_tmin, show_tmax):
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        day_tmin_color = "blue"
        day_tmax_color = "red"

        #Hover Effect
        TOOLTIPS = [
            ("Tag", "@x"),
            ("Temperatur", "@y")
        ]

        p = figure(sizing_mode="scale_both", min_width=min_width,
                   min_height=min_height, max_height=max_height,
                   max_width=max_width, title='Tagesansicht',
                   x_axis_label='Tag', y_axis_label='Temperatur',
                   toolbar_location=None, tools=["tap"])

        hover = HoverTool(tooltips=[("Tag", "@x"), ("Temperatur", "@y{0.0}°C")])

        p.add_tools(hover)

        legend_items = []

        #day TMAX plot
        if show_tmax:
            line_tmax = p.line(
                x = [day for day in averageTemperatures.keys()],
                y = [data['TMAX'] for data in averageTemperatures.values()],
                color=day_tmax_color,
                line_width=3
            )

            circle_tmax = p.circle(
                x = [day for day in averageTemperatures.keys()],
                y = [data['TMAX'] for data in averageTemperatures.values()],
                color=day_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Tag", [line_tmax, circle_tmax]))

        #day TMIN plot
        if show_tmin:
            line_tmin = p.line(
                x = [day for day in averageTemperatures.keys()],
                y = [data['TMIN'] for data in averageTemperatures.values()],
                color=day_tmin_color,
                line_width=4
            )

            circle_tmin = p.circle(
                x = [day for day in averageTemperatures.keys()],
                y = [data['TMIN'] for data in averageTemperatures.values()],
                color=day_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Tag", [line_tmin, circle_tmin]))

        legend = Legend(items=legend_items)
        p.add_layout(legend, 'right')

        script, div = components(p)

        return script, div