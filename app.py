#!/usr/bin/env python
# coding: utf-8

# Import Dependencies
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime as dt
import numpy as np
import random

#Set Global Variable for North Bay
getLocation = ['North Bay, Ontario','North Bay (CA), Ontario']


df_dg=pd.read_csv('Resources/dg.csv')
df_lf=pd.read_csv('Resources/lf.csv')
df_ws=pd.read_csv('Resources/ws.csv')

df_dg.set_index('Unnamed: 0', inplace=True)
df_lf.set_index('Unnamed: 0', inplace=True)
df_ws.set_index('Unnamed: 0', inplace=True)
df_dg['Date'] = pd.to_datetime(df_dg['Date'])
df_lf['Date'] = pd.to_datetime(df_lf['Date'])
df_ws['Date'] = pd.to_datetime(df_ws['Date'])

markdown_about = dcc.Markdown('''
- The North Bay Labour Market Dashboard was created by John Ellis to showcase data viualization and analytical abilities.  All data is retrieved from the Statistics Canada website via API calls.  The Data includes: 
- Wages, salaries and commissions of tax filers aged 15 years and over by sex and age group. [Adapted from Statistics Canada Table: 11-10-0072-01 Released: 2024-03-06](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110007201)   
- Labour force characteristics, annual. [Adapted from Statistics Canada Table: 14-10-0391-01 Released: 2024-01-05](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410039101)  
- Population estimates, July 1, by census metropolitan area and census agglomeration, 2021 boundaries. [Adpated from Statistics Canada Table: 17-10-0148-01 Released: 2024-05-22](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014801)  
*This does not constitute an endorsement by Statistics Canada of this product.*
''')


app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])
server = app.server

myTitle = 'Labour Market in North Bay Ontario'
app.title = myTitle

y_age = df_dg['Age group'].unique()

y_Population = df_lf['VALUE'].loc[(df_lf['Labour force characteristics'].isin(['Population'])) & (df_lf['Date'] > '2016-01-01')]
x_Date = df_lf.loc[(df_lf['Labour force characteristics'].isin(['Population'])) & (df_lf['Date'] > '2016-01-01')]


fig=px.bar(df_dg, x='VALUE', y='Age group', orientation='h',  template='simple_white', animation_frame='Year', color='Gender', labels={'VALUES':'Population'}, )
    
    

fig.update_layout(title='Population Pyramid - 2001 to 2023',
                  barmode = 'relative', 
                  bargap = 0.0, bargroupgap = 0, 
                  xaxis = dict(tickvals = [-3000, -2000, -1000, 
                                           0, 1000, 2000, 3000], 
                                
                              ticktext = ['3000', '2000', '1000', '0',  
                                          '1000', '2000', '3000'], 
                                
                              title = None, 
                              # title_font_size = 14
                              ),
                  template='simple_white',
                  width=990,
                  height=283,
                  margin=dict(l=1, r=1, t=40, b=10),
                  
                 ) 
fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 30)
fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 1,)

fig1 = px.bar(df_lf.loc[(df_lf['Labour force characteristics'].isin(['Employment', 'Not in labour force', 'Unemployment'])) & (df_lf['Date'] > '2016-01-01')],
                  x='Date',
                  y='VALUE',
                  title='Population Breakdown by Employment Characteristic',
                  labels={'VALUE': 'Persons in ,000s',
                         'Date':'Year',
                         'Labour force characteristics':'Characteristic'},
                  # size='VALUE',
                  template='simple_white',
                  width=990,
                  height=243,
                  color='Labour force characteristics',
                  # trendline='ols',
             )

# fig1.add_trace(go.Bar( name='Total Population', y=y_Population, x=x_Date, ))
                          
fig2 = px.scatter(df_ws.loc[(df_ws['Statistics']=='Median total income') 
               & (df_ws['Gender'].isin(['Both', 'Men+', 'Women+']))], 
                  template='simple_white', 
                  title = "Median Income in 000's with Trend",
                  x='Date', 
                  y='VALUE', 
                  labels = {'VALUE': '$,000s',
                           'Date':'Year',
                           # 'Sex':'Gender',
                           # 'Both sexes':'Average'
                           },
                  width=990,
                  height=243,
                  color='Gender', 
                  trendline="ols")

fig.update_layout(margin=dict(l=1, r=1, t=40, b=1))
fig1.update_layout(
    # plot_bgcolor='#ffffff',
    margin=dict(l=1, r=1, t=40, b=1))
fig2.update_layout(margin=dict(l=1, r=1, t=40, b=1),
                  )

# app layout
app.layout=dbc.Container([
    html.Div(
        [
            html.Div([
                html.H1([
                    html.Span("Welcome"),
                    html.Br(),
                    html.Span("to the North Bay Labour Market Dashboard!")
                ]),
                html.P("This Dashboard assists users in understanding the local labour market conditions.")
            ],
                     style={
                         "vertical-alignment": "top",
                         "height": 260
                     }),
            html.Div(
                [
                    # html.Div(dbc.Button(
                    #     # className='btn-group',
                    #     # inputClassName='btn-check',
                    #     # labelClassName="btn btn-outline-light",
                    #     # labelCheckedClassName="btn btn-light",
                    #     # options=[
                    #     #     {"label": "Graph", "value": 1},
                    #     #     {"label": "Table", "value": 2}
                    #     # ],
                    #     "Dashboard",
                    #     className="btn btn-dashboard",
                    #     color="primary",
                    #     # outline = True,
                    #     n_clicks=0, 
                        
                    #     ),
                    #          style={'width': 104,
                    #                'background':'fffff'}
                    # ),
                    html.Div([
                        dbc.Button(
                            "About",
                            className="btn btn-info",
                            n_clicks=0,
                            id='button-info'
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("About")),
                                dbc.ModalBody(markdown_about, className="MarkDown"),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close", id="close", className="ms-auto", n_clicks=0
                                    )
                                ),
                            ],
                            id="modal",
                            is_open=False,
                        ),                
                    ],
                             style={'width': 104})
                ],
                style={
                    'margin-left': 15,
                    'margin-right': 15,
                    'display': 'flex'
                }
            
            ),
            html.Div(
                [
                    html.Div(
                        [
                            # html.H2('Sex:'),
                            # dcc.Dropdown(
                            #     options=sex_list,
                            #     value=1,
                            #     clearable=True,
                            #     multi=True,
                            #     optionHeight=40
                            # )
                        ]
                    ),
                    html.Div(
                        [
                            # html.H2('Statistic to Plot:'),
                            # dcc.Dropdown(
                            #     options=UOM['Measure'],
                            #     value=1,
                            #     clearable=False,
                            #     multi=True,
                            #     optionHeight=40
                            # )
                        ]
                    ),                    
                    html.Div(
                        [
                            # html.H2('Income statistic:'),
                            # dcc.Dropdown(
                            #     options=income_statistic_list,
                            #     value=income_statistic_list[0],
                            #     clearable=True,
                            #     multi=True,
                            #     optionHeight=40
                                
                            # )
                        ]
                    )
            ],
                     style={
                         'margin-left': 15,
                         'margin-right': 15,
                         'margin-top': 30
                     }),
            
            html.Div(html.Img(src='assets/image.svg',
             style={
                 'margin-left': 15,
                 'margin-right': 15,
                 'margin-top': 30,
                 'width': 310,
                 'display':'flex'
             }
                             )
                    )
        ],
    style={
        'width': 340,
        'margin-left': 15,
        'margin-top': 15,
        'margin-bottom': 15
    }), 
    html.Div(
        [
            html.Div(dcc.Graph(figure=fig), style={'width': 990}),
            html.Div(dcc.Graph(figure=fig1), style={'width':990}),
            html.Div(dcc.Graph(figure=fig2), style={'width':990})
           
        ],
        
        style={
            'width': 990,
            'margin-top': 15,
            'margin-right': 15,
            'margin-bottom': 15,
            # 'display':'flex'
            }) 
    
    ],          
                      
   fluid = True,
   className='dashboard-container',
   style={'display':'flex'}
   )
@app.callback(
    Output("modal", "is_open"),
    [Input("button-info", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
if __name__ == "__main__":
    app.run_server(debug=False, jupyter_mode='_none')






