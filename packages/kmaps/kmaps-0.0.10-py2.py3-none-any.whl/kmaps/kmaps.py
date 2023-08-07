"""Main module."""

import random
import string
import ipyleaflet
import ipywidgets as widgets
import os


class Map(ipyleaflet.Map):
    """Class 'Map'

    Args:
        ipyleaflet (_type_): _description_
    """
    def __init__(self, center = [37.5, 127], zoom = 8, **kwargs):
        """Create a Map.

        Args:
            center (list, optional): A coordinate representing the center of the map. Defaults to `[37.5, 127]`
            zoom (int, optional): Zoom level. Defaults to 8
        """        
        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True
        super().__init__(center = center, zoom = zoom, **kwargs) # inherited from the parent, in this case, ipyleaflet
        
        if 'layers_control' not in kwargs:
            kwargs['layers_control'] = True
        
        if kwargs['layers_control']:
            self.add_layers_control()

        #self.add_states_dropdown()
        self.add_search_control()


    
    #['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California']

    def add_states_dropdown(self, position = 'bottomright', **kwargs):
        """Add a dropdown widget to move to selected state to the map.

        Args:
            position (str, optional): Position of the widget. Defaults to 'bottomright'.
        """            
        states_list = [('Initial Location', self.center), 
            ('Alabama', [32.78, -86.83]), ('Alaska', [64.07, -152.28]), 
            ('Arizona', [34.27, -111.66]), ('Arkansas', [34.89, -92.44]),
            ('California', [37.18, -119.47]), ('Colorado', [39.00, -105.55]),
            ('Connecticut', [41.62, -72.73]), ('Delaware', [38.99, -75.51]),
            ('District of Columbia', [38.91, -77.01]), ('Florida', [28.63, -82.45]),
            ('Georgia', [32.64, -83.44]), ('Hawaii', [20.29, -156.37]),
            ('Idaho', [44.35, -114.61]), ('Illinois', [40.04, -89.20]),
            ('Indiana', [39.89, -86.28]), ('Iowa', [42.08, -93.50]),
            ('Kansas', [38.49, -98.38]), ('Kentucky', [37.53, -85.30]),
            ('Louisiana', [31.07, -92.00]), ('Maine', [45.37, -69.24]),
            ('Maryland', [39.06, -76.80]), ('Massachusetts', [42.26, -71.81]),
            ('Michigan', [44.35, -85.41]), ('Minnesota', [46.28, -94.31]),
            ('Mississippi', [32.74, -89.67]), 
            ('Montana', [47.05, -109.63]), ('Nebraska', [41.54, -99.80]),
            ('Nevada', [39.33, -116.63]), ('New Hampshire', [43.68, -71.58]),
            ('New Jersey', [40.19, -74.67]), ('New Mexico', [34.41, -106.11]),
            ('New York', [42.95, -75.53]), ('North Carolina', [35.56, -79.39]),
            ('North Dakota', [47.45, -100.47]), ('Ohio', [40.29, -82.79]),
            ('Oklahoma', [35.59, -97.49]), ('Oregon', [43.93, -120.56]),
            ('Pennsylvania', [40.88, -77.80]), ('Rhode Island', [41.68, -71.56]),
            ('South Carolina', [33.92, -80.90]), ('South Dakota', [44.44, -100.23]),
            ('Tennessee', [35.86, -86.35]), ('Texas', [31.48, -99.33]),
            ('Utah', [39.31, -111.67]), ('Vermont', [44.07, -72.67]),
            ('Virginia', [37.52, -78.85]), ('Washington', [47.38, -120.45]),
            ('West Virginia', [38.64, -80.62]), ('Wisconsin', [44.62, -89.99]),
            ('Wyoming', [43.00, -107.55])]
        states_dropdown = widgets.Dropdown(
            options = states_list,
            value = self.center,
            description = 'States',
            style = {'description_width': 'initial'}
        )

        states_control = ipyleaflet.WidgetControl(widget = states_dropdown, position = position)
        self.add(states_control)
        
        widgets.link((self, 'center'), (states_dropdown, 'value'))


    def add_base_dropdown(self, position = 'bottomright', **kwargs):
        """Add a dropdown widget to select a basemap.

        Args:
            position (str, optional): Position of the widget. Defaults to 'bottomright'.
        """        
        base_dropdown = widgets.Dropdown(
            options = ['Satellite', 'Roadmap'],
            value = None,
            description = 'Basemap',
        )

        basemap_ctrl = ipyleaflet.WidgetControl(widget = base_dropdown, position = position)

        def change_basemap(change):
            if change['new']:
                self.add_basemap(base_dropdown.value)
        
        base_dropdown.observe(change_basemap, 'value')

        self.add(basemap_ctrl)



    def add_search_control(self, position = 'topleft', **kwargs):
        """Add a search control panel to the map.

        Args:
            position (str, optional): The location of the search control panel. Defaults to 'topleft'.
        """        
        if 'url' not in kwargs:
            kwargs['url'] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
        
        search_control = ipyleaflet.SearchControl(position = position, **kwargs)
        self.add_control(search_control)


    def add_draw_control(self, position = 'topleft', **kwargs):
        """Add a draw control panel to the map.

        Args:
            position (str, optional): The location of the draw control panel. Defaults to 'topleft'.
        """        
        draw_control = ipyleaflet.DrawControl(position = position, **kwargs)
        self.add_control(draw_control)


    def add_layers_control(self, position = 'topright', **kwargs):
        """Add a layers control panel to the map.

        Args:
            position (str, optional): The location of the layers control panel. Defaults to 'topright'.
        """        
        layers_control = ipyleaflet.LayersControl(position = position, **kwargs)
        self.add_control(layers_control)


    def add_tile_layer(self, url, name, attribution = '', **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): xyz url of the tile layer.
            name (str): A name of the layer that would be displayed on the map.
            attribution (str, optional): A name of the attribution. Defaults to ''.
        """        
        tile_layer = ipyleaflet.TileLayer(
            url = url,
            name = name,
            attribution = attribution,
            **kwargs
        )
        self.add_layer(tile_layer)
    

    def add_basemap(self, basemap, **kwargs):
        """Add a base map to the map.

        Args:
            basemap (str): xyz url of the base map.

        Raises:
            ValueError: Error message will be raised if the url is not available.
        """
        import xyzservices.providers as xyz

        if basemap.lower() == 'roadmap':
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name = basemap, **kwargs)
        elif basemap.lower() == 'satellite':
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name = basemap, **kwargs)
        else:
            try:
                basemap = eval(f'xyz.{basemap}')
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name = basemap, attribution = attribution, **kwargs)
            except:
                raise ValueError(f'{basemap} is not found')


    def add_geojson(self, data, name = 'GeoJSON', **kwargs):
        """Add a geojson file to the map.

        Args:
            data (str): A name of the geojson file.
            name (str, optional): A layer name of the geojson file to be displayed on the map. Defaults to 'GeoJSON'.
        """        
        if isinstance(data, str):
            import json
            with open(data, 'r') as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data = data, name = name, **kwargs)
        self.add_layer(geojson)
    
    def add_shp(self, data, name = 'Shapefile', **kwargs):
        """Add a ESRI shape file to the map.

        Args:
            data (str): A name of the shape file.
            name (str, optional): A layer name of the shape file to be displayed on the map. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name = name, **kwargs)

    def add_raster(self, url, name = 'Raster', fit_bounds = True, **kwargs):
        """Add a raster file to the map.

        Args:
            url (str): An url of the raster image.
            name (str, optional): A layer name of the raster to be displayed on the map. Defaults to 'Raster'.
            fit_bounds (bool, optional): Move a display of the map to the raster image location. Defaults to True.
        """        
        import httpx

        titiler_endpoint = 'https://titiler.xyz'
        
        # get a bbox
        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        # get a url
        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r['tiles'][0]

        self.add_tile_layer(url = tile, name = name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)
        
    def add_local_raster(self, filename, name = 'local raster', **kwargs):
        try:
            import localtileserver
        except ImportError:
            raise ImportError('')
    


    def add_vector(
        self,
        filename,
        layer_name = 'Vector data',
        **kwargs,
    ):
        import os
        if not filename.startswith('http'):
            filename = os.path.abspath(filename)
        else:
            filename = github_raw_url(filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.shp':
            self.add_shp(
                filename,
                layer_name
            )
        elif ext in ['.json', '.geojson']:
            self.add_geojson(
                filename,
                layer_name
            )
        else:
            geojson = vector_to_geojson(
                filename,
                bbox = bbox,
                mask = mask,
                rows = rows,
                epsg = '4326',
                **kwargs,
            )

            self.add_geojson(
                geojson,
                layer_name
            )
    
    def add_image(self, url, width, height, position = 'bottomright'):
        """Add an image file to the map.

        Args:
            url (str): An url of the image.
            width (float): width of the image to be displayed
            height (float): height of the image to be displayed
            position (_type_, optional): Position argument. Defaults to 'bottomright'.
        """        
        from ipyleaflet import WidgetControl
        import ipywidgets as widgets

        widget = widgets.HTML(value = f'<img src="{url}" width = "{width}" height = "{height}">')
        control = WidgetControl(widget = widget, position = position)
        self.add(control)




    def to_streamlit(self, width=None, height=600, scrolling=False, **kwargs):
        ####### just copied from leafmap
        """Renders map figure in a Streamlit app.
        Args:
            width (int, optional): Width of the map. Defaults to None.
            height (int, optional): Height of the map. Defaults to 600.
            responsive (bool, optional): Whether to make the map responsive. Defaults to True.
            scrolling (bool, optional): If True, show a scrollbar when the content is larger than the iframe. Otherwise, do not show a scrollbar. Defaults to False.
        Returns:
            streamlit.components: components.html object.
        """

        try:
            import streamlit.components.v1 as components

            # if responsive:
            #     make_map_responsive = """
            #     <style>
            #     [title~="st.iframe"] { width: 100%}
            #     </style>
            #     """
            #     st.markdown(make_map_responsive, unsafe_allow_html=True)
            return components.html(
                self.to_html(), width=width, height=height, scrolling=scrolling
            )

        except Exception as e:
            raise Exception(e)

    def to_html(
        self,
        outfile=None,
        title="My Map",
        width="100%",
        height="880px",
        add_layer_control=True,
        **kwargs,
    ):
        ####### just copied from leafmap
        """Saves the map as an HTML file.
        Args:
            outfile (str, optional): The output file path to the HTML file.
            title (str, optional): The title of the HTML file. Defaults to 'My Map'.
            width (str, optional): The width of the map in pixels or percentage. Defaults to '100%'.
            height (str, optional): The height of the map in pixels. Defaults to '880px'.
            add_layer_control (bool, optional): Whether to add the LayersControl. Defaults to True.
        """
        try:
            save = True
            if outfile is not None:
                if not outfile.endswith(".html"):
                    raise ValueError("The output file extension must be html.")
                outfile = os.path.abspath(outfile)
                out_dir = os.path.dirname(outfile)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
            else:
                outfile = os.path.abspath(random_string() + ".html")
                save = False

            '''
            if add_layer_control and self.layer_control is None:
                layer_control = ipyleaflet.LayersControl(position="topright")
                self.layer_control = layer_control
                self.add(layer_control)
            '''
            
            before_width = self.layout.width
            before_height = self.layout.height

            if not isinstance(width, str):
                print("width must be a string.")
                return
            elif width.endswith("px") or width.endswith("%"):
                pass
            else:
                print("width must end with px or %")
                return

            if not isinstance(height, str):
                print("height must be a string.")
                return
            elif not height.endswith("px"):
                print("height must end with px")
                return

            self.layout.width = width
            self.layout.height = height

            self.save(outfile, title=title, **kwargs)

            self.layout.width = before_width
            self.layout.height = before_height

            if not save:
                out_html = ""
                with open(outfile) as f:
                    lines = f.readlines()
                    out_html = "".join(lines)
                os.remove(outfile)
                return out_html

        except Exception as e:
            raise Exception(e)
    


def generate_random_string(length, upper = False, digit = False, punc = False):
    """Generates a random string of a given length.

    Args:
        length (int): A length of the string.
        upper (bool, optional): Whether you would like to contain upper case alphabets in your string pool or not. Defaults to False.
        digit (bool, optional): Whether you would like to contain digits in your string pool or not. Defaults to False.
        punc (bool, optional): Whether you would like to contain punctuations in your string pool or not. Defaults to False.

    Returns:
        str: Generated random string.
    """
    chars = string.ascii_lowercase
    if upper:
        chars += string.ascii_uppercase
    if digit:
        chars += string.digits
    if punc:
        chars += string.punctuation
    
    result_str = ''.join(random.choice(chars) for i in range(length))
    return result_str


def generate_lucky_number(length = 2):
    """Generates a random number of a given length.

    Args:
        length (int, optional): A length of the number. Defaults to 2.

    Returns:
        int: Generated random number.
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    result_str = int(result_str)
    return result_str


def euclidean_dist(first_coord, second_coord):
    """Calculates an Euclidean distance between two coordinates.

    Args:
        first_coord (list): A coordinate of the first point. Should have 2 length. 
        second_coord (list): A coordinate of the second point. Should have 2 length. 

    Returns:
        int: Calculated Euclidean distance.
    """
    import math
    for coord in [first_coord, second_coord]:
        if not isinstance(coord, (list, tuple)) or len(coord) != 2:
            raise ValueError('The coordinates must be lists or tuples of length 2.')
        for element in coord:
            if not isinstance(element, (int, float)):
                raise ValueError('The elements of the coordinates must be integers or floats.')
                
    x_diff = first_coord[0] - second_coord[0]
    y_diff = first_coord[1] - second_coord[1]
    dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
    return dist