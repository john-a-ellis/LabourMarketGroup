#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
from stats_can import StatsCan
import dash_bootstrap_components as dbc
import datetime as dt
# import plotly.graph_objects as go
import numpy as np
import random
sc = StatsCan()
pd.options.display.max_colwidth = 255


# In[2]:


#set storage location for Stats Can Data
sc = StatsCan(data_folder="Resources")


# In[3]:


#Set Global Variable for North Bay
getLocation = ['North Bay, Ontario','North Bay (CA), Ontario']


# In[4]:


df = sc.table_to_df("17-10-0148-01") # demographic data

df=df.loc[df['GEO'].isin(getLocation)]

df.rename(columns = {'REF_DATE':'Date'}, inplace=True)

df=df.replace(to_replace='90 years and older', value= '90 years +')


# In[5]:


gender_list=df['Gender'].unique().tolist()
dg_date_list= df['Date'].unique().tolist()
mylist = df['Age group'].unique().tolist()


# In[6]:


age_list = []
for i in mylist:
    # print(i)
    if i.find('to') != -1:
        age_list.append(i)
    elif i.find('and') != -1:
        age_list.append(i)
    elif i.find('+') != -1:
        age_list.append(i)
        

age_list.remove('0 to 14 years')
age_list.remove('65 years and older')
age_list.remove('15 to 64 years')


# In[7]:


df_dg = df.loc[(df['GEO'].isin(getLocation)) & (df['Age group'].isin(age_list)) & (df['Gender'].isin(gender_list))]


# In[8]:


#Import Data from Stats Canada
# df = sc.table_to_df("14-10-0137-01") # Count of Persons claiming EI per week
# df.rename(columns = {'REF_DATE':'Date'}, inplace=True)
# df_ei = df.loc[(df['GEO'].isin(getLocation)) & (df['Age group'] == '15 years and over')]
# df_ei.rename(columns = {'VALUE':'Claimants'}, inplace=True)
df = sc.table_to_df("14-10-0391-01") # Labour force characteristics by year for 5 years
df.rename(columns = {'REF_DATE':'Date'}, inplace=True)
df_lf= df.loc[df['GEO'].isin((getLocation))]
df = sc.table_to_df("11-10-0072-01") # Wages Salearies and  commissions of tax filers by sex and age group
df.rename(columns = {'REF_DATE':'Date'}, inplace=True)
df_ws= df.loc[(df['GEO'].isin(getLocation)) & (df['Age group']=='Ages 15 years and over')]
df=''


# In[9]:


#replacing 
df_ws['Sex'].replace('Both sexes', 'Both', inplace =True) 
df_ws['Sex'].replace('Males', 'Men+', inplace=True)
df_ws['Sex'].replace('Females', 'Women+', inplace=True)
df_ws.rename(columns={'Sex':'Gender'}, inplace=True)


# In[10]:


#set up drop lists 
# sex_list = df_ei['Sex'].unique().tolist()
# beneficiary_list = df_ei['Beneficiary detail'].unique().tolist()
characteristic_list= df_lf['Labour force characteristics'].unique().tolist()
# age_group_list = df_ei['Age group'].unique().tolist()
income_statistic_list = df_ws['Statistics'].unique().tolist()



# In[11]:


UOM = df_ws[['Statistics', 'UOM']]
UOM=UOM.drop_duplicates()


# In[12]:


UOM=UOM.rename(columns={'Statistics':'Measure'})


# In[13]:


temp_df=df_lf[['Labour force characteristics', 'UOM']]
temp_df=temp_df.drop_duplicates()
temp_df=temp_df.rename(columns={'Labour force characteristics':'Measure'})


# In[14]:


UOM=pd.concat([UOM, temp_df], ignore_index = True)


# In[15]:


# beneficiary_list = df_ei['Beneficiary detail'].unique().tolist()


# In[16]:


# temp_df=df_ei[['Beneficiary detail', 'UOM']]
# temp_df=temp_df.drop_duplicates()
# temp_df=temp_df.replace(to_replace='Persons', value='Claimants')
# temp_df=temp_df.rename(columns={'Beneficiary detail':'Measure'})


# In[17]:


# creating negative values for women for population pyramid.
df_dg['VALUE'] = df_dg.apply(lambda row: row['VALUE']*-1 if row['Gender']=='Women+' else row['VALUE'], axis=1)


# In[18]:


df_dg['Year']=pd.DatetimeIndex(df_dg['Date']).year


# In[19]:


df_dg.drop(df_dg.index[df_dg['Gender']=='Total - gender'], inplace=True)
df_dg['Gender'].unique()


# In[20]:


df_dg.to_csv('Resources/dg.csv')
df_lf.to_csv('Resources/lf.csv')
df_ws.to_csv('Resources/ws.csv')


# In[21]:


df_lf.info()


# In[22]:


df_dg=pd.read_csv('Resources/dg.csv')
df_lf=pd.read_csv('Resources/lf.csv')
df_ws=pd.read_csv('Resources/ws.csv')


# In[23]:


df_dg.set_index('Unnamed: 0', inplace=True)
df_lf.set_index('Unnamed: 0', inplace=True)
df_ws.set_index('Unnamed: 0', inplace=True)
df_dg['Date'] = pd.to_datetime(df_dg['Date'])
df_lf['Date'] = pd.to_datetime(df_lf['Date'])
df_ws['Date'] = pd.to_datetime(df_ws['Date'])


# In[24]:


markdown_about = dcc.Markdown('''
- The North Bay Labour Market Dashboard was created by John Ellis to showcase data viualization and analytical abilities.  All data is retrieved from the Statistics Canada website via API calls.  The Data includes: 
- Wages, salaries and commissions of tax filers aged 15 years and over by sex and age group. [Adapted from Statistics Canada Table: 11-10-0072-01 Released: 2024-03-06](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110007201)   
- Labour force characteristics, annual. [Adapted from Statistics Canada Table: 14-10-0391-01 Released: 2024-01-05](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410039101)  
- Population estimates, July 1, by census metropolitan area and census agglomeration, 2021 boundaries. [Adpated from Statistics Canada Table: 17-10-0148-01 Released: 2024-05-22](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014801)  
*This does not constitute an endorsement by Statistics Canada of this product.*
''')


# In[25]:


app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])
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
            # html.Div(
            #     [
            #         html.H2('Output 1:'),
            #         html.Div(className='Output'),
            #         html.H2('Output 2:'),
            #         html.Div(html.H3("Selected Value"), className='Output')
            #     ],
            #       style={'width': 200})
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
    app.run_server(debug=True, port=8050)




# In[ ]:





# In[ ]:




