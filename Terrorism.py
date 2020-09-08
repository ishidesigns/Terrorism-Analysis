
#importing the libraries
import pandas as pd
import webbrowser

import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate


# Global variables
app = dash.Dash()


def load_data():
  dataset_name = "global_terror.csv"

  #this line we use to hide some warnings which gives by pandas
  pd.options.mode.chained_assignment = None
  
  global df
  df = pd.read_csv(dataset_name)
  
  global month_list
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
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [x for x in range(1, 32)]


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  global country_list
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()

  global state_list
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

  global city_list
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  
  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
  global dd_style
  dd_style = {
                   'padding':'10px',
                   'borderRadius': '30px',
                   'color': 'green',
                   'fontSize':'20px',
                   'width':'80%',
                   'marginLeft':'10%'
            }
  
  global icon_style
  icon_style = {
                    'width':'50px',
                    'height':'50px',
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
  webbrowser.open_new('http://127.0.0.1:8050/')

# Layout of your page
def app_ui():
  main_layout = html.Div(
      style = {'backgroundColor':'pink'},
      children =[
              html.H1(children = 'Terrorism Analysis with Insights', id='Main_title',
                      style = {
                        'textAlign':'center',
                        'color':'red',
                        'textDecoration':'underline',
                        'fontFamily':'Trebuchet MS, sans-serif',
                        'fontSize': '40px'
                        }
                ),
              html.P(style = para_style,
                children = [
                    html.H2(style = tx_style, children = 'What is Terrorism?'),
                    html.P(style = para_style, children = 'The unlawful use of force and violence against persons or property to intimidate or coerce a government, the civilian population, or any segment thereof, in furtherance of political or social objectives'),
                    html.H2(style = tx_style, children = 'About the Project'),
                    html.P(style = para_style, children = 'This project is based on Global Terrorism Database'),
                    html.P(style = para_style, children = 'The Global Terrorism Database (GTD) is the most comprehensive unclassified database of terrorist attacks in the world. The National Consortium for the Study of Terrorism and Responses to Terrorism (START) makes the GTD available in an effort to improve understanding of terrorist violence, so that it can be more readily studied and defeated. The GTD is produced by a dedicated team of researchers and technical staff.'),
                    html.P(style = para_style, children = 'The GTD is an open-source database, which provides information on domestic and international terrorist attacks around the world since 1970, and now includes more than 1.9L events. For each event, a wide range of information is available, including the date and location of the incident, the weapons used, nature of the target, the number of casualties, and – when identifiable – the group or individual responsible.')
                ]),
    
              html.H2(style = {'padding':'20px'},
                  children = ['To view the Maps and Charts, Use the given tabs for reference:']),
                          dcc.Tabs(id="Tabs", value="Map",children=[
                              dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
                                  dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
                                      dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                                      dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                                      ]),
              html.Div(style = {
                              'backgroundImage':'url("/assets/Background.jpg")',
                              'backgroundSize':'cover'
                          },
                  children = [
                  dcc.Dropdown(
                      id='month', 
                        options=month_list,
                        placeholder='Select Month',
                        style = dd_style,
                        multi = True
                          ),
                  dcc.Dropdown(
                        id='date', 
                        placeholder='Select Day',
                        style = dd_style,
                        multi = True
                          ),
                  dcc.Dropdown(
                        id='region-dropdown', 
                        options=region_list,
                        placeholder='Select Region',
                        style = dd_style,
                        multi = True
                          ),
                  dcc.Dropdown(
                        id='country-dropdown', 
                        options=[{'label': 'All', 'value': 'All'}],
                        placeholder='Select Country',
                        style = dd_style,
                        multi = True
                          ),
                  dcc.Dropdown(
                        id='state-dropdown', 
                        options=[{'label': 'All', 'value': 'All'}],
                        placeholder='Select State or Province',
                        style = dd_style,
                        multi = True
                          ),
                  dcc.Dropdown(
                        id='city-dropdown', 
                        options=[{'label': 'All', 'value': 'All'}],
                        placeholder='Select City',
                        style = dd_style,
                        multi = True
                          ),
                  dcc.Dropdown(
                        id='attacktype-dropdown', 
                        options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                        placeholder='Select Attack Type',
                        style = dd_style,
                        multi = True
                          ),
        
                  html.H3('Select the Year', id='year_title', style = {'color':'white','padding':'20px'}),
                  dcc.RangeSlider(
                            id='year-slider',
                            min=min(year_list),
                            max=max(year_list),
                            value=[min(year_list),max(year_list)],
                            marks=year_dict,
                            step=None
                              ),
                  html.Hr()
                  ])
              ]),
                dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
                    dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
                        dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
                        dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
                        dcc.Dropdown(id="Chart_Dropdown", 
                             options = chart_dropdown_values, 
                             placeholder="Select option", 
                             style = dd_style,
                             value = "region_txt"), 
                        html.Br(),
                        dcc.Input(id="search", placeholder="Search Filter"),
                        html.Hr(),
                        html.H3('Select Year Range'),
                        dcc.RangeSlider(
                            id='cyear_slider',
                            min=min(year_list),
                            max=max(year_list),
                            value=[min(year_list),max(year_list)],
                            marks=year_dict,
                            step=None
                              ),
                        html.Hr()
                      ])
             ]),
            dcc.Loading(html.Div(id = "graph-object", children ="Graph will be shown here")),
      
            html.Footer(id = 'pageFooter', 
                    style = {
                        'backgroundColor':'black',
                        'height':'130px',
                        'textAlign':'center'
                        },
                    children = [
                        html.H2(children = "CONTACT  US",
                                 style = {
                                     'color':'white',
                                     'textDecoration':'underline'
                                     }),
                        html.Img(src = "/assets/fb.png",style = icon_style),
                        dcc.Link(children = [
                                   html.Img(src = "/assets/instagram.png",
                                            style = icon_style)
                                   ],
                               href = "https://www.instagram.com/addicted__soul/"
                               ),
                        html.Img(src = "/assets/twitter.png",style = icon_style),
                        html.Br(),
                        html.Label(children = "Terms & Services | Privacy Policy",
                                 style = {'color':'white'}),
                        ])
      ])
        
  return main_layout


# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('cyear_slider', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )

def def_app_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
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
        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)


@app.callback(
  Output("date", "options"),
  [Input("month", "value")])

def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option
  
@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_regionIndia(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of your Project
def main():
  print("Welcome")
  load_data()
  
  open_browser()
  
  global app
  app.layout = app_ui()
  app.title = "Terrorism Analysis with Insights"
  app.run_server() # debug=True

  print("Thanks")
  df = None
  app = None


if __name__ == '__main__':
    main()

