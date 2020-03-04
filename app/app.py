import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Global Vaiables to control what data is stored
schema = pd.read_csv('/home/ubuntu/data/indexed_schema.csv')
cd = schema
selectable_object_class = cd.object_class.unique()


# Main App
app.layout = html.Div([
    html.H1("Auto cArchive", style={"textAlign": "center"}),

#     html.Div([
#         html.Div([
#             html.Label('Select Object Class'),
#             dcc.Dropdown(
#                 id='object-dropdown',
#                 options=[{'label': i, 'value': i} for i in selectable_object_class],
#                 value=selectable_object_class
#             )
#         ],
#         style={'width': '33%', 'display': 'inline-block'})#,

#     ]),

    html.Div([
        dcc.Graph(
            id='count_of_objects'
            #,hoverData={'points':}
        )]
    )
])

def create_pie_chart(dff, title):
    return {
        'data': [dict(
            type="pie",
            values=dff['sample_id'],
            labels=dff['object_class']
        )],
        'layout': {
                'height': 700,
                'margin': {'l': 60, 'b': 40, 'r': 20, 't': 100},
                'annotations': [{
                    'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom',
                    'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                    'align': 'center',
                    'bgcolor': 'rgba(255, 255, 255, 0.5)',
                    'text': title
            }]
        }
    }



@app.callback(
    Output('count_of_objects', 'figure'),
        [Input('object-dropdown', 'value')]
        )
def update_pie(instance):
    selected_data = cd
    title_str = "Count of the object class"
    grouped = selected_data.groupby('object_class').count().reset_index()


    return create_pie_chart(grouped, title_str)

def isSelected(in_val):
    return not isinstance(in_val, list) and (in_val is not None)

if __name__ == '__main__':
#     app.run_server(debug=True) #if you run from local machine
     app.run_server(host="0.0.0.0") #from EC2 instance