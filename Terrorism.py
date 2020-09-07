
import pandas as pd
import dash   # !pip install dash
import dash_html_components as html
from dash.dependencies import Input, State, Output
import dash_core_components as dcc

import plotly.graph_objects as go
import plotly.express as px
import webbrowser
from dash.exceptions import PreventUpdate

# Global Variables
app = dash.Dash()  # Creating your object

def load_data():
    dataset = 'global_terror.csv'
    
    global df
    df = pd.read_csv(dataset)
    
    global idf
    filter1 = (df['country_txt'] == "India")
    idf = df[filter1]
    
    month = {
           "January":1,
           "February": 2,
           "March": 3,
           "April":4,
           "May":5,
           "June":6,
           "July": 7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }

    global month_list
    month_list= [{"label":key, "value":values} for key,values in month.items()]
    
    global date_list
    date_list = [{"label":x, "value":x} for x in range(1, 32)] 
    
    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
    
    temp_list = sorted(df['country_txt'].unique().tolist())
    
    global country_list
    country_list = [{"label": str(i), "value": str(i)}  for i in temp_list ]
    
    global state_list
    state_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
    
    global city_list
    city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
    
    global attack_list
    attack_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
    
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    #print(year_list)

    global year_dict
    year_dict = {str(year): str(year) for year in year_list}
    
    global chart_dropdown_values
    chart_dropdown_values ={"Terrorist Organisation":'gname',
                            "Target Nationality" : 'natlty1_txt',
                            "Target Type" : 'targtype1_txt',
                            "Type of Attack" : 'attacktype1_txt',
                            "Weapon Type" : 'weaptype1_txt',
                            "Region":'region_txt',
                            "Country Attacked" : 'country_txt'}
    
    chart_dropdown_values = [{"label" : keys, "value" : value} for keys, value in chart_dropdown_values.items() ]
    
    global tab_style
    tab_style = {
                    'border':'5px solid blue',
                    'backgroundColor': '#abff57'
                 }
    
    global dd_style
    dd_style = {
                   'padding':'10px',
                   'borderRadius': '30px',
                   'color': 'green',
                   'fontSize':'20px',
                   'width':'80%',
                   'marginLeft':'10%'
                }
    
    global tx_style
    tx_style = {
                    'fontSize':'24px',
                    'fontWeight':'bold',
                    'textAlign':'center',
                    'width':'80%',
                    'marginLeft':'10%',
                    'textDecoration':'underline'
                }
    
    global para_style
    para_style = {
                    'fontSize':'18px',
                    'textAlign':'center',
                    'width':'80%',
                    'marginLeft':'10%'
                }
    
def open_browser():
    # Opening the Browser
    webbrowser.open_new('http://127.0.0.1:8050/')

def app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div(
    style = {'backgroundColor':'pink'},
    children = [
    html.H1('Terrorism Analysis with Insights', id='Main_title',
            style = {
                'textAlign':'center',
                'color':'red',
                'textDecoration':'underline',
                'fontFamily':'Trebuchet MS, sans-serif',
                'fontSize': '40px'
                }),
    
    html.P(style = para_style,
        children = [
            html.H2(style = tx_style, children = 'What is Terrorism?'),
            html.P(style = para_style, children = 'The unlawful use of force and violence against persons or property to intimidate or coerce a government, the civilian population, or any segment thereof, in furtherance of political or social objectives'),
            html.H2(style = tx_style, children = 'About the Project'),
            html.P(style = para_style, children = 'This project is based on Global Terrorism Database'),
            html.P(style = para_style, children = 'The Global Terrorism Database (GTD) is the most comprehensive unclassified database of terrorist attacks in the world. The National Consortium for the Study of Terrorism and Responses to Terrorism (START) makes the GTD available via this site in an effort to improve understanding of terrorist violence, so that it can be more readily studied and defeated. The GTD is produced by a dedicated team of researchers and technical staff.'),
            html.P(style = para_style, children = 'The GTD is an open-source database, which provides information on domestic and international terrorist attacks around the world since 1970, and now includes more than 1.9L events. For each event, a wide range of information is available, including the date and location of the incident, the weapons used, nature of the target, the number of casualties, and – when identifiable – the group or individual responsible.')
        ]),
    
    html.H2(style = {'padding':'20px'},
        children = ['To view the Maps and Charts, Use the given tabs for reference:']),
    
    dcc.Tabs(id="Tabs", value="mainTab",
             style = {'padding':'20px'},
             children=[
              dcc.Tab(label="Map tool" ,id="MapTool",value="MapTab", style = tab_style,
                 children=[]),
              dcc.Tab(label = "Chart Tool", id="ChartTool", value="ChartTab",style = tab_style, 
                  children=[])
              ]
             ),
    
    html.Br(),
    ]
    )
        
    return main_layout

@app.callback(
    dash.dependencies.Output('MapTool','children'),
    [dash.dependencies.Input('Tabs','value')]
    )
def MapSubtabs(value):
    if value =='MapTab':
        return dcc.Tabs(id = "MapSubtabs", value = "Mapsubtab",children = [
              dcc.Tab(label="World Map tool", id="WorldM", value="WMtab", style = tab_style, 
                children = [
                  html.Div(style = {
                      'backgroundImage':'url("/assets/Background.jpg")',
                      'backgroundSize':'cover'
                      },
                  children = [
                      
                  html.Br(),
                
                  dcc.Dropdown(
                  id='monthDD', 
                  style = dd_style,
                  options=month_list,
                  placeholder='Select Month',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='dateDD', 
                  style = dd_style,
                  options=date_list,
                  placeholder='Select Day',
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='regionDD', 
                  style = dd_style,
                  options=region_list,
                  placeholder='Select Region',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='countryDD', 
                  style = dd_style,
                  options=country_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select Country',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='stateDD', 
                  style = dd_style,
                  options=state_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select State or Province',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='cityDD', 
                  style = dd_style,
                  options=city_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select City',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='attacktypeDD',
                  style = dd_style,
                  options=attack_list,
                  placeholder='Select Attack Type',
                  value = [],
                  multi = True
                  ),
                html.H5(children = 'Select the Year', id='yearSelect', 
                        style = {'color':'white', 'fontSize':'20px'}),
        
                  dcc.RangeSlider(
                  id='yearRS',
                  min=min(year_list),
                  max=max(year_list),
                  value=[min(year_list),max(year_list)],
                  marks=year_dict
                  )
                  ]),
                  
                html.Hr(),
                
                dcc.Graph(id='graphSample', children = ["World Map is loading"])
                ]),
              
              dcc.Tab(label="India Map tool", id="IndiaMap", value="IMtab", style = tab_style, 
                children =[
                 html.Div(style = {
                      'backgroundImage':'url("/assets/Background.jpg")',
                      'backgroundSize':'cover'
                      },
                  children = [
                      
                  html.Br(),
                
                  dcc.Dropdown(
                  id='monthDD1', 
                  style = dd_style,
                  options=month_list,
                  placeholder='Select Month',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='dateDD1', 
                  style = dd_style,
                  options=date_list,
                  placeholder='Select Day',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='regionDD1', 
                  style = dd_style,
                  options=region_list,
                  placeholder='Select Region',
                  value = ['South Asia'],
                  disabled = 'disabled',
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='countryDD1', 
                  style = dd_style,
                  options=country_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select Country',
                  value = ['India'],
                  disabled = 'disabled',
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='stateDD1', 
                  style = dd_style,
                  options=state_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select State or Province',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='cityDD1', 
                  style = dd_style,
                  options=city_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select City',
                  value = [],
                  multi = True
                  ),
            
                  dcc.Dropdown(
                  id='attacktypeDD1', 
                  style = dd_style,
                  options=attack_list,
                  placeholder='Select Attack Type',
                  value = [],
                  multi = True
                  ),
                  
                html.H5(children = 'Select the Year', id='yearSelect1', 
                        style = {'color':'white', 'fontSize':'20px','padding':'20px'}),
        
                  dcc.RangeSlider(
                  id='yearRS1',
                  min=min(year_list),
                  max=max(year_list),
                  value=[min(year_list),max(year_list)],
                  marks=year_dict
                  )
                  ]),
           
                html.Hr(),
                
                dcc.Graph(id='graphSample1', children = ["India Map is loading"])
                ])
            ])

@app.callback(
    dash.dependencies.Output('ChartTool','children'),
    [dash.dependencies.Input('Tabs','value')]
    )
def ChartSubtabs(value):
    if value == 'ChartTab':
        return dcc.Tabs(id = "ChartSubtabs", value = "Chartsubab",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WCtab",style = tab_style,
                children = [
                  
                  dcc.Dropdown(
                          id = 'categoryDD',
                          style = dd_style,
                          placeholder = 'Select a Category',
                          options = chart_dropdown_values, 
                          value='region_txt'
                          ),
                  
                  html.Br(),
                  
                  html.Label('Filter By: '),
                  
                  dcc.Input(
                          id = 'ipFilter',
                          placeholder = 'Filter'
                          ),
                  
                  html.Hr(),
                  
                  dcc.Graph(id = 'ChartContent', children = ['Chart is loading'])
                  ]),
              
              
              dcc.Tab(label="India Chart tool", id="IndiaC", value="ICtab", style = tab_style, 
                children = [
                  
                  dcc.Dropdown(
                          id = 'categoryDD1',
                          style = dd_style,
                          placeholder = 'Select a Category',
                          options = chart_dropdown_values, 
                          value='region_txt'
                          ),
                  
                  html.Br(),
                  
                  html.Label('Filter By: '),
                  
                  dcc.Input(
                          id = 'ipFilter1',
                          placeholder = 'Filter'
                          ),
                  
                  html.Hr(),
                  
                  dcc.Graph(id = 'ChartContent1', children = ['Chart is loading'])
              ])
        ])
              
#callback for world chart
@app.callback(
    dash.dependencies.Output('ChartContent', 'figure'),
    [
     dash.dependencies.Input('categoryDD','value'),
     dash.dependencies.Input('ipFilter', 'value')
     ]
    )
def WorldChart_UI(category_val, search_val):
    if category_val is not None:
        if search_val is not None:
            new_df = df.groupby('iyear')[category_val].value_counts().reset_index(name='count')
            new_df = new_df[new_df[category_val].str.contains(search_val, case=False)]
        else:
            new_df = df.groupby('iyear')[category_val].value_counts().reset_index(name='count')
        
    else:
        raise PreventUpdate
            
    chartFigure = px.area(new_df, x='iyear', y='count', color = category_val)
    fig = chartFigure
    
    return fig

#callback for india chart
@app.callback(
    dash.dependencies.Output('ChartContent1', 'figure'),
    [
     dash.dependencies.Input('categoryDD1','value'),
     dash.dependencies.Input('ipFilter1', 'value')
     ]
    )
def IndiaChart_UI(category_val, search_val):
    if category_val is not None:
        if search_val is not None:
            new_df = idf.groupby('iyear')[category_val].value_counts().reset_index(name='count')
            new_df = new_df[new_df[category_val].str.contains(search_val, case=False)]
        else:
            new_df = idf.groupby('iyear')[category_val].value_counts().reset_index(name='count')
        
    else:
        raise PreventUpdate
            
    chartFigure = px.area(new_df, x='iyear', y='count', color = category_val)
    fig = chartFigure
    
    return fig
    
    
# Callback for world Map
@app.callback(
    dash.dependencies.Output('graphSample', 'figure'),
    [
    dash.dependencies.Input('monthDD', 'value'),
    dash.dependencies.Input('dateDD', 'value'),
    dash.dependencies.Input('regionDD', 'value'),
    dash.dependencies.Input('countryDD', 'value'),
    dash.dependencies.Input('stateDD', 'value'),
    dash.dependencies.Input('cityDD', 'value'),
    dash.dependencies.Input('attacktypeDD', 'value'),
    dash.dependencies.Input('yearRS', 'value')
    ]
    )
def WorldMap_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value):
  
  print("Data Type of month value = " , str(type(month_value)))
  print("Data of month value = " , month_value)

  print("Data Type of Day value = " , str(type(date_value)))
  print("Data of Day value = " , date_value)

  print("Data Type of region value = " , str(type(region_value)))
  print("Data of region value = " , region_value)

  print("Data Type of country value = " , str(type(country_value)))
  print("Data of country value = " , country_value)

  print("Data Type of state value = " , str(type(state_value)))
  print("Data of state value = " , state_value)

  print("Data Type of city value = " , str(type(city_value)))
  print("Data of city value = " , city_value)

  print("Data Type of Attack value = " , str(type(attack_value)))
  print("Data of Attack value = " , attack_value)

  print("Data Type of year value = " , str(type(year_value)))
  print("Data of year value = " , year_value)

  global figure
  figure = go.Figure() #creates blank figure
    
  # year_filter
  year_range = range(year_value[0], year_value[1]+1)
  new_df = df[df["iyear"].isin(year_range)]
    
  # month_filter
  if month_value==[] or month_value is None:
        pass
  else:
        if date_value==[] or date_value is None:
            new_df = new_df[new_df["imonth"].isin(month_value)]
        else:
            new_df = new_df[new_df["imonth"].isin(month_value)
                            & (new_df["iday"].isin(date_value))]
              
              
  # region, country, state, city filter
  if region_value==[] or region_value is None:
        pass
  else:
        if country_value==[] or country_value is None :
            new_df = new_df[new_df["region_txt"].isin(region_value)]
        else:
            if state_value == [] or state_value is None:
                new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value))]
            else:
                if city_value == [] or city_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value)) &
                                (new_df["provstate"].isin(state_value))]
                else:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value)) &
                                    (new_df["provstate"].isin(state_value))&
                                    (new_df["city"].isin(city_value))]
    
  if attack_value == [] or attack_value is None:
        pass
  else:
        new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]
      

  if new_df.shape[0]:
        pass
  else: 
        new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
        
        new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
    
  figure = px.scatter_mapbox(new_df,
                  lat = "latitude", 
                  lon = "longitude",
                  color = "attacktype1_txt",
                  hover_data = ["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                  zoom = 2
                  )                       
  figure.update_layout(mapbox_style = "open-street-map",
              autosize = True,
              margin = dict(l = 0, r = 0, t = 25, b = 20),
              )
  
  return figure

#Callback for India Map
@app.callback(
    dash.dependencies.Output('graphSample1', 'figure'),
    [
    dash.dependencies.Input('monthDD1', 'value'),
    dash.dependencies.Input('dateDD1', 'value'),
    dash.dependencies.Input('regionDD1', 'value'),
    dash.dependencies.Input('countryDD1', 'value'),
    dash.dependencies.Input('stateDD1', 'value'),
    dash.dependencies.Input('cityDD1', 'value'),
    dash.dependencies.Input('attacktypeDD1', 'value'),
    dash.dependencies.Input('yearRS1', 'value')
    ]
    )
def IndiaMap_ui(month_val, date_val, region_val, country_val, state_val, city_val, attack_val, year_val):
  
  print("Data Type of month value = " , str(type(month_val)))
  print("Data of month value = " , month_val)

  print("Data Type of Day value = " , str(type(date_val)))
  print("Data of Day value = " , date_val)

  print("Data Type of region value = " , str(type(region_val)))
  print("Data of region value = " , region_val)

  print("Data Type of country value = " , str(type(country_val)))
  print("Data of country value = " , country_val)

  print("Data Type of state value = " , str(type(state_val)))
  print("Data of state value = " , state_val)

  print("Data Type of city value = " , str(type(city_val)))
  print("Data of city value = " , city_val)

  print("Data Type of Attack value = " , str(type(attack_val)))
  print("Data of Attack value = " , attack_val)

  print("Data Type of year value = " , str(type(year_val)))
  print("Data of year value = " , year_val)
  
  global figure
  figure = go.Figure() #creates blank figure
    
  # year_filter
  year_range = range(year_val[0], year_val[1]+1)
  new_df = df[df["iyear"].isin(year_range)]
    
  # month_filter
  if month_val==[] or month_val is None:
        pass
  else:
        if date_val==[] or date_val is None:
            new_df = new_df[new_df["imonth"].isin(month_val)]
        else:
            new_df = new_df[new_df["imonth"].isin(month_val)
                            & (new_df["iday"].isin(date_val))]
              
              
  # region, country, state, city filter
  if region_val == [] or region_val is None:
        pass
  else:
        if country_val==[] or country_val is None :
            new_df = new_df[new_df["region_txt"].isin(region_val)]
        else:
            if state_val == [] or state_val is None:
                new_df = new_df[(new_df["region_txt"].isin(region_val))&
                                (new_df["country_txt"].isin(country_val))]
            else:
                if city_val == [] or city_val is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_val))&
                                (new_df["country_txt"].isin(country_val)) &
                                (new_df["provstate"].isin(state_val))]
                else:
                    new_df = new_df[(new_df["region_txt"].isin(region_val))&
                                    (new_df["country_txt"].isin(country_val)) &
                                    (new_df["provstate"].isin(state_val))&
                                    (new_df["city"].isin(city_val))]
    
  if attack_val == [] or attack_val is None:
        pass
  else:
        new_df = new_df[new_df["attacktype1_txt"].isin(attack_val)]
      

  if new_df.shape[0]:
        pass
  else: 
        new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
        
        new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
    
  figure = px.scatter_mapbox(new_df,
                  lat = "latitude", 
                  lon = "longitude",
                  color = "attacktype1_txt",
                  hover_data = ["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                  zoom = 2
                  )                       
  figure.update_layout(mapbox_style = "open-street-map",
              autosize = True,
              margin = dict(l = 0, r = 0, t = 25, b = 20),
              )
  
  return figure
  
@app.callback(
  Output("dateDD", "options"),
  [
  Input("monthDD", "value")
  ]
  )
def update_date(month):
    date_list = [x for x in range(1, 32)]
    day1 = False
    day2 = False
    day3 = False
    
    if month == []:
        return []
    else:
        for num in month:
            if num in [1,3,5,7,8,10,12]:
                day1 = True
        
            elif num in [4,6,9,11]:
                day2 = True
        
            elif num == 2:
                day3 = True
                
        if day1 == True:
            return [{"label":m, "value":m} for m in date_list]
        elif day2 == True:
            return [{"label":m, "value":m} for m in date_list[:-1]]
        else:
            return [{"label":m, "value":m} for m in date_list[:-2]]


@app.callback(
    Output('countryDD', 'options'),
    [
    Input('regionDD', 'value')
    ]
    )
def RegionToCountry(region_value):
  return[{"label": str(i), "value": str(i)}  for i in df[df['region_txt'].isin(region_value)] ['country_txt'].unique().tolist() ]


@app.callback(
    Output('stateDD', 'options'),
    [
    Input('countryDD', 'value')
    ]
    )   
def CountryToState(country_value):
  return [{"label": str(i), "value": str(i)}  for i in df[df['country_txt'].isin(country_value)] ['provstate'].unique().tolist() ]


@app.callback(
    Output('cityDD', 'options'),
    [
    Input('stateDD', 'value')
    ]
    )
def StateToCity(state_value):
  return [{"label": str(i), "value": str(i)}  for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist() ]

@app.callback(
  Output("dateDD1", "options"),
  [
  Input("monthDD1", "value")
  ]
  )
def update_date(month):
    date_list = [x for x in range(1, 32)]
    day1 = False
    day2 = False
    day3 = False
    
    if month == []:
        return []
    else:
        for num in month:
            if num in [1,3,5,7,8,10,12]:
                day1 = True
        
            elif num in [4,6,9,11]:
                day2 = True
        
            elif num == 2:
                day3 = True
                
        if day1 == True:
            return [{"label":m, "value":m} for m in date_list]
        elif day2 == True:
            return [{"label":m, "value":m} for m in date_list[:-1]]
        else:
            return [{"label":m, "value":m} for m in date_list[:-2]]


@app.callback(
    Output('stateDD1', 'options'),
    [
    Input('countryDD1', 'value')
    ]
    )
def CountryToState(country_value):
  return [{"label": str(i), "value": str(i)}  for i in df[df['country_txt'].isin(country_value)] ['provstate'].unique().tolist() ]


@app.callback(
    Output('cityDD1', 'options'),
    [
    Input('stateDD1', 'value')
    ]
    )
def StateToCity(state_value):
  return [{"label": str(i), "value": str(i)}  for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist() ]


def main():
    print("Welcome to the Project Season 3 ")   
    
    load_data()
    open_browser()
    
    global app
    app.layout = app_ui()  # blank Container Page
    app.title = "Terrorism Analysis"
    app.run_server()
    
    print("Thanks for using my Project ")
    # Industry Best Practices 
    app = None 
    df = None 

if __name__ == '__main__' :
    main()

"""
option = []
for i in df:
    option.append(i)

option
"""