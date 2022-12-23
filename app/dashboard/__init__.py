import dash
from dash import dcc, html, Input, Output
import os
import lasio
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# r"C:\Users\clone\OneDrive\javaproject\web\final_git\app\static\files\"

def getfile(filename):
     path = "C:\\Users\\clone\\OneDrive\\javaproject\\web\\final_git\\app\\static\\files\\" + filename
     file1 = lasio.read(path)
     lasdf = file1.df()
     lasdf['WELL'] = file1.well.WELL.value
     lasdf = lasdf.reset_index()
     return lasdf, file1.well.WELL.value

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) 
            for i in range(min(len(dataframe), max_rows))
        ])
    ])

def init_dashboard(server):
     
     dash_app1 = dash.Dash(
		server= server,
		routes_pathname_prefix='/dash1/',
		external_stylesheets=[
		"/static/dist/css/styles.css",
          "https://fonts.googleapis.com/css?family=Lato",	
		],
	)
     
     dash_app1.layout = html.Div([
          dcc.Dropdown(
			['A10.las','A15.las'],
			'A10',
			id = 'input'
		),
          html.H3(id = 'name1'),
          dcc.Graph(
			id = 'graph',
			# figure= fig
		),
    		# generate_table(getfile())
      ]
	)
     
     @dash_app1.callback(
		Output('graph','figure'),
		Input('input','value'))
     def update_table(input_value):
          df = getfile(input_value)[0]
          fig = make_subplots(rows= 1, cols = 4, shared_yaxes= True)
          fig.add_trace(go.Scatter(x=df['PERM'], y=df['DEPT'], name= 'PERM'), row = 1, col = 1)
          fig.add_trace(go.Scatter(x=df['GAMMA'], y=df['DEPT'], name='GAMMA'), row = 1, col = 2 )
          fig.add_trace(go.Scatter(x=df['POROSITY'], y=df['DEPT'], name = 'POROSITY'), row = 1, col = 3 )
          fig.add_trace(go.Scatter(x=df['NETGROSS'], y=df['DEPT'], name= 'NETGROSS'), row = 1, col = 4 )
          
          fig.update_xaxes(title_text = 'PERM', row = 1, col = 1)
          fig.update_xaxes(title_text = 'GAMMA', row = 1, col = 2)
          fig.update_xaxes(title_text = 'POROSITY', row = 1, col = 3)
          fig.update_xaxes(title_text = 'NETGROSS', row = 1, col = 4)
          return fig
     
     @dash_app1.callback(
		Output('name1','children'),
		Input('input','value')
	)
     def get_well_name(input_value):
          return f'bảng dữ liệu của giếng {input_value}'
     
     return dash_app1.server

