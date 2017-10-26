
Inspiration: World 3D
=====================

The purpose of this example is to demonstrate you what is possible to do
when doing interactive maps. 3D globe and presenting data on top of such
is a nice way to visualize data as it presents the surface of the Earth
correctly (unlike e.g. when using Mercator projection).

This is based on `this Folium
example <https://github.com/python-visualization/folium/blob/d2c495b871c09dac656b4fc4f8b153e36f1eed14/examples/Hacking_folium_3D_globe.ipynb>`__

-  Create couple of classes that makes possible to create the 3D globe.
   We haven't talked anything about classes in Python during the course,
   so don't mind if you don't understand what is happening

.. code:: python

    import folium
    from folium.features import Template

    class Map3d(folium.Map):
    
        def __init__(self, location=None, width='100%', height='100%', left='0%',
                     top='0%', position='relative', tiles='OpenStreetMap', API_key=None,
                     max_zoom=18, min_zoom=1, zoom_start=10, attr=None, min_lat=-90,
                     max_lat=90, min_lon=-180, max_lon=180, detect_retina=False, crs='EPSG3857'):
            super(Map3d, self).__init__(
                location=location, width=width, height=height,
                left=left, top=top, position=position, tiles=tiles,
                API_key=API_key, max_zoom=max_zoom, min_zoom=min_zoom,
                zoom_start=zoom_start, attr=attr, min_lat=min_lat,
                max_lat=max_lat, min_lon=min_lon, max_lon=max_lon,
                detect_retina=detect_retina, crs=crs
            )
            self._template = Template(u"""
            {% macro header(this, kwargs) %}
                <script src="https://www.webglearth.com/v2/api.js"></script>
                <style> #{{this.get_name()}} {
                    position : {{this.position}};
                    width : {{this.width[0]}}{{this.width[1]}};
                    height: {{this.height[0]}}{{this.height[1]}};
                    left: {{this.left[0]}}{{this.left[1]}};
                    top: {{this.top[0]}}{{this.top[1]}};
                    }
                </style>
            {% endmacro %}
            {% macro html(this, kwargs) %}
                <div class="folium-map" id="{{this.get_name()}}" ></div>
            {% endmacro %}
    
            {% macro script(this, kwargs) %}
    
                var southWest = L.latLng({{ this.min_lat }}, {{ this.min_lon }});
                var northEast = L.latLng({{ this.max_lat }}, {{ this.max_lon }});
                var bounds = L.latLngBounds(southWest, northEast);
    
                var {{this.get_name()}} = WE.map('{{this.get_name()}}', {
                                               center:[{{this.location[0]}},{{this.location[1]}}],
                                               zoom: {{this.zoom_start}},
                                               maxBounds: bounds,
                                               layers: [],
                                               crs: L.CRS.{{this.crs}}
                                             });
            {% endmacro %}
            """)
    
    
    class TileLayer3d(folium.TileLayer):
    
        def __init__(self, tiles='OpenStreetMap', min_zoom=1, max_zoom=18, attr=None,
                     API_key=None, detect_retina=False, name=None, overlay=False, control=True):
            super(TileLayer3d, self).__init__(
                tiles=tiles, min_zoom=min_zoom, max_zoom=max_zoom,
                attr=attr, API_key=API_key, detect_retina=detect_retina,
                name=name, overlay=overlay, control=control
            )
            self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = WE.tileLayer(
                    '{{this.tiles}}',
                    {
                        maxZoom: {{this.max_zoom}},
                        minZoom: {{this.min_zoom}},
                        attribution: '{{this.attr}}',
                        detectRetina: {{this.detect_retina.__str__().lower()}}
                        }
                    ).addTo({{this._parent.get_name()}});
    
            {% endmacro %}
            """)
                

-  Create the globe

.. code:: python

    # Initialize the 3D globe 
    m = Map3d(location=[60.25, 24.8], tiles=None, zoom_start=1)
    
    # Add a Map Tiles on top of the Globe
    m.add_child(TileLayer3d(tiles='CartoDB positron'))
    
    # Show it
    m




.. raw:: html

    <div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><iframe src="data:text/html;base64,PCFET0NUWVBFIGh0bWw+CjxoZWFkPiAgICAKICAgIDxtZXRhIGh0dHAtZXF1aXY9ImNvbnRlbnQtdHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04IiAvPgogICAgPHNjcmlwdD5MX1BSRUZFUl9DQU5WQVMgPSBmYWxzZTsgTF9OT19UT1VDSCA9IGZhbHNlOyBMX0RJU0FCTEVfM0QgPSBmYWxzZTs8L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL3VucGtnLmNvbS9sZWFmbGV0QDEuMC4xL2Rpc3QvbGVhZmxldC5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9hamF4Lmdvb2dsZWFwaXMuY29tL2FqYXgvbGlicy9qcXVlcnkvMS4xMS4xL2pxdWVyeS5taW4uanMiPjwvc2NyaXB0PgogICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vYm9vdHN0cmFwLzMuMi4wL2pzL2Jvb3RzdHJhcC5taW4uanMiPjwvc2NyaXB0PgogICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL0xlYWZsZXQuYXdlc29tZS1tYXJrZXJzLzIuMC4yL2xlYWZsZXQuYXdlc29tZS1tYXJrZXJzLmpzIj48L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9sZWFmbGV0Lm1hcmtlcmNsdXN0ZXIvMS4wLjAvbGVhZmxldC5tYXJrZXJjbHVzdGVyLXNyYy5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbGVhZmxldC5tYXJrZXJjbHVzdGVyLzEuMC4wL2xlYWZsZXQubWFya2VyY2x1c3Rlci5qcyI+PC9zY3JpcHQ+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vdW5wa2cuY29tL2xlYWZsZXRAMS4wLjEvZGlzdC9sZWFmbGV0LmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9jc3MvYm9vdHN0cmFwLXRoZW1lLm1pbi5jc3MiIC8+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vZm9udC1hd2Vzb21lLzQuNi4zL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9sZWFmbGV0Lm1hcmtlcmNsdXN0ZXIvMS4wLjAvTWFya2VyQ2x1c3Rlci5EZWZhdWx0LmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbGVhZmxldC5tYXJrZXJjbHVzdGVyLzEuMC4wL01hcmtlckNsdXN0ZXIuY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL3Jhd2dpdC5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIiAvPgogICAgPHN0eWxlPmh0bWwsIGJvZHkge3dpZHRoOiAxMDAlO2hlaWdodDogMTAwJTttYXJnaW46IDA7cGFkZGluZzogMDt9PC9zdHlsZT4KICAgIDxzdHlsZT4jbWFwIHtwb3NpdGlvbjphYnNvbHV0ZTt0b3A6MDtib3R0b206MDtyaWdodDowO2xlZnQ6MDt9PC9zdHlsZT4KICAgIAogICAgICAgICAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly93d3cud2ViZ2xlYXJ0aC5jb20vdjIvYXBpLmpzIj48L3NjcmlwdD4KICAgICAgICAgICAgPHN0eWxlPiAjbWFwXzFlYjRkMWYyZjI2MTQ5M2FiOTQ4NjRiYjg4ZDk4ZDgzIHsKICAgICAgICAgICAgICAgIHBvc2l0aW9uIDogcmVsYXRpdmU7CiAgICAgICAgICAgICAgICB3aWR0aCA6IDEwMC4wJTsKICAgICAgICAgICAgICAgIGhlaWdodDogMTAwLjAlOwogICAgICAgICAgICAgICAgbGVmdDogMC4wJTsKICAgICAgICAgICAgICAgIHRvcDogMC4wJTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgPC9zdHlsZT4KICAgICAgICAKPC9oZWFkPgo8Ym9keT4gICAgCiAgICAKICAgICAgICAgICAgPGRpdiBjbGFzcz0iZm9saXVtLW1hcCIgaWQ9Im1hcF8xZWI0ZDFmMmYyNjE0OTNhYjk0ODY0YmI4OGQ5OGQ4MyIgPjwvZGl2PgogICAgICAgIAo8L2JvZHk+CjxzY3JpcHQ+ICAgIAogICAgCgogICAgICAgICAgICB2YXIgc291dGhXZXN0ID0gTC5sYXRMbmcoLTkwLCAtMTgwKTsKICAgICAgICAgICAgdmFyIG5vcnRoRWFzdCA9IEwubGF0TG5nKDkwLCAxODApOwogICAgICAgICAgICB2YXIgYm91bmRzID0gTC5sYXRMbmdCb3VuZHMoc291dGhXZXN0LCBub3J0aEVhc3QpOwoKICAgICAgICAgICAgdmFyIG1hcF8xZWI0ZDFmMmYyNjE0OTNhYjk0ODY0YmI4OGQ5OGQ4MyA9IFdFLm1hcCgnbWFwXzFlYjRkMWYyZjI2MTQ5M2FiOTQ4NjRiYjg4ZDk4ZDgzJywgewogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY2VudGVyOls2MC4yNSwyNC44XSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHpvb206IDEsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBtYXhCb3VuZHM6IGJvdW5kcywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxheWVyczogW10sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjcnM6IEwuQ1JTLkVQU0czODU3CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSk7CiAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHRpbGVfbGF5ZXJfN2ViNTQ1NjllN2QzNGMzZDg0YjkyYjI1ZWY2MzkzMDMgPSBXRS50aWxlTGF5ZXIoCiAgICAgICAgICAgICAgICAnaHR0cHM6Ly9jYXJ0b2RiLWJhc2VtYXBzLXtzfS5nbG9iYWwuc3NsLmZhc3RseS5uZXQvbGlnaHRfYWxsL3t6fS97eH0ve3l9LnBuZycsCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgbWF4Wm9vbTogMTgsCiAgICAgICAgICAgICAgICAgICAgbWluWm9vbTogMSwKICAgICAgICAgICAgICAgICAgICBhdHRyaWJ1dGlvbjogJyhjKSA8YSBocmVmPSJodHRwOi8vd3d3Lm9wZW5zdHJlZXRtYXAub3JnL2NvcHlyaWdodCI+T3BlblN0cmVldE1hcDwvYT4gY29udHJpYnV0b3JzIChjKSA8YSBocmVmPSJodHRwOi8vY2FydG9kYi5jb20vYXR0cmlidXRpb25zIj5DYXJ0b0RCPC9hPiwgQ2FydG9EQiA8YSBocmVmID0iaHR0cDovL2NhcnRvZGIuY29tL2F0dHJpYnV0aW9ucyI+YXR0cmlidXRpb25zPC9hPicsCiAgICAgICAgICAgICAgICAgICAgZGV0ZWN0UmV0aW5hOiBmYWxzZQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzFlYjRkMWYyZjI2MTQ5M2FiOTQ4NjRiYjg4ZDk4ZDgzKTsKCiAgICAgICAgCjwvc2NyaXB0Pg==" style="position:absolute;width:100%;height:100%;left:0;top:0;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>


Pretty cool, isn't it! =)

