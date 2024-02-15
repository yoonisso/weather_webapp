from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, Legend, TapTool, CustomJS, OpenURL

class DiagramPloter:
    @staticmethod
    def plotYearDiagram(averageTemperatures, chosen_views, url):
        """
        Plots a yearly temperature diagram.

        Parameters:
            averageTemperatures (dict): A dictionary containing average temperatures data.
            chosen_views (dict): A dictionary specifying which temperature views to include.
            url (str): The base URL to navigate to upon clicking on a data point.

        Returns:
            tuple: A tuple containing Bokeh script and div components.
        """

        # Setup colors, dimensions, and tooltips
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

        amount_chosen_views = 0
        for season, data in chosen_views.items():
            for value in data.values():
                if value == False:
                    amount_chosen_views += 1
        amount_chosen_views = 10 - amount_chosen_views

        if amount_chosen_views < 4:
            line_width = 3
            circle_size = 9
        elif amount_chosen_views <= 7:
            line_width = 2
            circle_size = 7
        else:
            line_width = 1
            circle_size = 5

        TOOLTIPS = [
            ("Jahr", "@x"),
            ("Temperatur", "@y")
        ]

        # Create Bokeh figure
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
                line_width=line_width
            )

            circle_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMAX'] for data in averageTemperatures.values()],
                color=year_tmax_color,
                size=circle_size
            )
            legend_items.append(("TMAX Jahr", [line_tmax, circle_tmax]))

        #year TMIN plot
        if chosen_views['year']['TMIN']:
            line_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMIN'] for data in averageTemperatures.values()],
                color=year_tmin_color,
                line_width=line_width
            )

            circle_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['year']['TMIN'] for data in averageTemperatures.values()],
                color=year_tmin_color,
                size=circle_size
            )
            legend_items.append(("TMIN Jahr", [line_tmin, circle_tmin]))

        #Spring TMAX
        if chosen_views['spring']['TMAX']:
            line_spring_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMAX'] for data in averageTemperatures.values()],
                color=spring_tmax_color,
                line_width=line_width
            )

            circle_spring_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMAX'] for data in averageTemperatures.values()],
                color=spring_tmax_color,
                size=circle_size
            )
            legend_items.append(("TMAX Frühling", [line_spring_tmax, circle_spring_tmax]))

        #Spring TMIN
        if chosen_views['spring']['TMIN']:
            line_spring_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMIN'] for data in averageTemperatures.values()],
                color=spring_tmin_color,
                line_width=line_width
            )

            circle_spring_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['spring']['TMIN'] for data in averageTemperatures.values()],
                color=spring_tmin_color,
                size=circle_size
            )
            legend_items.append(("TMIN Frühling", [line_spring_tmin, circle_spring_tmin]))

        #Summer TMAX
        if chosen_views['summer']['TMAX']:
            line_summer_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMAX'] for data in averageTemperatures.values()],
                color=summer_tmax_color,
                line_width=line_width
            )

            circle_summer_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMAX'] for data in averageTemperatures.values()],
                color=summer_tmax_color,
                size=circle_size
            )
            legend_items.append(("TMAX Sommer", [line_summer_tmax, circle_summer_tmax]))

        #summer TMIN
        if chosen_views['summer']['TMIN']:
            line_summer_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMIN'] for data in averageTemperatures.values()],
                color=summer_tmin_color,
                line_width=line_width
            )

            circle_summer_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['summer']['TMIN'] for data in averageTemperatures.values()],
                color=summer_tmin_color,
                size=circle_size
            )
            legend_items.append(("TMIN Sommer", [line_summer_tmin, circle_summer_tmin]))

        #Fall TMAX
        if chosen_views['fall']['TMAX']:
            line_fall_tmax = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMAX'] for data in averageTemperatures.values()],
                color=fall_tmax_color,
                line_width=line_width
            )

            circle_fall_tmax = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMAX'] for data in averageTemperatures.values()],
                color=fall_tmax_color,
                size=circle_size
            )
            legend_items.append(("TMAX Herbst", [line_fall_tmax, circle_fall_tmax]))

        #Fall TMIN
        if chosen_views['fall']['TMIN']:
            line_fall_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMIN'] for data in averageTemperatures.values()],
                color=fall_tmin_color,
                line_width=line_width
            )

            circle_fall_tmin = p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['fall']['TMIN'] for data in averageTemperatures.values()],
                color=fall_tmin_color,
                size=circle_size
            )
            legend_items.append(("TMIN Herbst", [line_fall_tmin, circle_fall_tmin]))

        #Winter TMAX
        if chosen_views['winter']['TMAX']:
            line_winter_tmax=p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMAX'] for data in averageTemperatures.values()],
                color=winter_tmax_color,
                line_width=line_width
            )

            circle_winter_tmax=p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMAX'] for data in averageTemperatures.values()],
                color=winter_tmax_color,
                size=circle_size
            )
            legend_items.append(("TMAX Winter", [line_winter_tmax, circle_winter_tmax]))

        #Winter TMIN
        if chosen_views['winter']['TMIN']:
            line_winter_tmin = p.line(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMIN'] for data in averageTemperatures.values()],
                color=winter_tmin_color,
                line_width=line_width
            )

            circle_winter_tmin= p.circle(
                x = [year for year in averageTemperatures.keys()],
                y = [data['winter']['TMIN'] for data in averageTemperatures.values()],
                color=winter_tmin_color,
                size=circle_size
            )
            legend_items.append(("TMIN Winter", [line_winter_tmin, circle_winter_tmin]))

        # Add legebd to the plot
        legend = Legend(items=legend_items)
        p.add_layout(legend, 'right')

        # Setup tap callback to navigate to URLs
        tap_callback = CustomJS(args=dict(url=url), code="""
            const selected_index = cb_data.source.selected.indices[0];
            const year = cb_data.source.data['x'][selected_index];
            
            const new_url = url + "/" + year;
            
            window.location.href = new_url;
            
            cb_data.source.selected.indices = [];
            """)

        taptool = p.select(type=TapTool)
        taptool.callback = tap_callback

        # Setup Bokeh components and return
        script, div = components(p)

        return script, div

    @staticmethod
    def plotMonthDiagram(averageTemperatures, show_tmin, show_tmax, url):
        """
        Plots a monthly temperature diagram.

        Parameters:
            averageTemperatures (dict): A dictionary containing average temperatures data.
            show_tmin (bool): Whether to show minimum temperatures.
            show_tmax (bool): Whether to show maximum temperatures.
            url (str): The base URL to navigate to upon clicking on a data point.

        Returns:
            tuple: A tuple containing Bokeh script and div components.
        """

        # Setup colors, dimensions, and tooltips
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        month_tmin_color = "blue"
        month_tmax_color = "red"

        TOOLTIPS = [
            ("Monat", "@x"),
            ("Temperatur", "@y")
        ]

        # Create Bokeh figure
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

        # Create legend
        legend = Legend(items=legend_items)
        p.add_layout(legend, 'right')

        # Setup tap callback to navigate to URLs
        tap_callback = CustomJS(args=dict(url=url), code="""
            const selected_index = cb_data.source.selected.indices[0];
            const month = cb_data.source.data['x'][selected_index];
            
            const new_url = url + "/" + month;
            
            window.location.href = new_url;
            
            cb_data.source.selected.indices = [];
            """)

        taptool = p.select(type=TapTool)
        taptool.callback = tap_callback

        # Generate Bokeh components and return
        script, div = components(p)

        return script, div

    @staticmethod
    def plotDayDiagram(averageTemperatures, show_tmin, show_tmax):
        """
        Plots a daily temperature diagram.

        Parameters:
            averageTemperatures (dict): A dictionary containing average temperatures data.
            show_tmin (bool): Whether to show minimum temperatures.
            show_tmax (bool): Whether to show maximum temperatures.

        Returns:
            tuple: A tuple containing Bokeh script and div components.
        """

        # Setup colors, dimensions, and tooltips
        min_width = 300
        min_height = 300
        max_width = 800
        max_height = 600

        day_tmin_color = "blue"
        day_tmax_color = "red"

        TOOLTIPS = [
            ("Tag", "@x"),
            ("Temperatur", "@y")
        ]

        # Create the Bokeh figure
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
            y_values = []
            for data in averageTemperatures.values():
                if 'TMAX' in data.keys():
                    y_values.append(data['TMAX'])
                else:
                    y_values.append(None)

            line_tmax = p.line(
                x = [day for day in averageTemperatures.keys()],
                y = y_values,
                color=day_tmax_color,
                line_width=3
            )

            circle_tmax = p.circle(
                x = [day for day in averageTemperatures.keys()],
                y = y_values,
                color=day_tmax_color,
                size=10
            )
            legend_items.append(("TMAX Tag", [line_tmax, circle_tmax]))

        #day TMIN plot
        if show_tmin:
            y_values = []
            for data in averageTemperatures.values():
                if 'TMIN' in data.keys():
                    y_values.append(data['TMIN'])
                else:
                    y_values.append(None)
                
                    
            line_tmin = p.line(
                x = [day for day in averageTemperatures.keys()],
                y = y_values,
                color=day_tmin_color,
                line_width=4
            )

            circle_tmin = p.circle(
                x = [day for day in averageTemperatures.keys()],
                y = y_values,
                color=day_tmin_color,
                size=10
            )
            legend_items.append(("TMIN Tag", [line_tmin, circle_tmin]))

        # Create Legend
        legend = Legend(items=legend_items)
        p.add_layout(legend, 'right')

         # Generate Bokeh components and return
        script, div = components(p)

        return script, div