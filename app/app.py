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
print(schema.head(5))
cd = schema
selectable_object_class = cd.object_class.unique()
# selectable_neighborhoods = cd.neighborhood.unique()
# selectable_streets = cd.street.unique()
# cities = ["Los Angeles", "San Francisco", "New York City", "Denver",
#           "Las Vegas", "Austin"]

# Main App
app.layout = html.Div([
    html.H1("Auto cArchive", style={"textAlign": "center"}),

    #html.Div({
    #    html.Label('Enter City'),
    #    dcc.Dropdown(
    #        id='major-city-dropdown',
    #        options=[{'label': i, 'value': i} for i in cities],
    #        value="Los Angeles"
    #    )
    #}),

    html.Div([
        html.Div([
            html.Label('Select Object Class'),
            dcc.Dropdown(
                id='object-dropdown',
                options=[{'label': i, 'value': i} for i in selectable_object_class],
                value=selectable_object_class
            )
        ],
        style={'width': '33%', 'display': 'inline-block'})#,

#         html.Div([
#             html.Label('Enter Neighborhood'),
#             dcc.Dropdown(
#                 id='neighborhood-dropdown',
#                 options=[{'label': i, 'value': i} for i in selectable_neighborhoods],
#                 value=selectable_neighborhoods
#             )],
#             style={'width': '33%', 'display': 'inline-block'}
#         ),

#         html.Div([
#             html.Label('Enter Street'),
#             dcc.Dropdown(
#                 id='street-dropdown',
#                 options=[{'label': i, 'value': i} for i in selectable_streets],
#                 value=selectable_streets
#             )
#         ],
#         style={'width': '33%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(
            id='count_of_objects'
            #,hoverData={'points':}
        )]
    )#,

    #html.Div([
    #    dcc.Graph(
    #        id='assessor-values-by-type-bars'
    #        #,hoverData={'points':}
    #    )]
    #)
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

# def create_bar_chart(dff, title):
#     return {
#         'data': [dict(
#             type="pie",
#             y=dff['count'],
#             x=dff['object_class']
#         )],
#         'layout': {
#                 'height': 700,
#                 'margin': {'l': 60, 'b': 40, 'r': 20, 't': 100},
#             'xaxis': {
#             'title': "Object Class"
#             },
#             'yaxis': {
#             'title': "Count",
#             #'tickprefix': "$"
#             },
#             'annotations': [{
#             'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom',
#             'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#             'align': 'center',
#             'bgcolor': 'rgba(255, 255, 255, 0.5)',
#             'text': title
#             }]
#         }
#     }

# def create_time_series(dff, title):
#     return {
#         'data': [dict(
#             x=dff['object_class'].unique(),
#             y=(dff['avg_land_value'] + dff['avg_improvement_value']),
#             mode='lines+markers'
#         )],
#         'layout': {
#             'height': 700,
#             'margin': {'l': 40, 'b': 40, 'r': 20, 't': 10},
#             'annotations': [{
#                 'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                 'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                 'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                 'text': title
#             }]
#         }
#     }


@app.callback(
    Output('count_of_objects', 'figure'),
#     [
        [Input('object-dropdown', 'value')]#,
#      Input('neighborhood-dropdown', 'value'),
#      Input('street-dropdown', 'value')]
        )
def update_pie(instance):
    selected_data = cd
    title_str = "Count of the object class"
#     if isSelected(city):
#         selected_data = selected_data.loc[selected_data['city'] == city]
#         title_str = city + " Assessor Value"
#     if isSelected(neighborhood):
#         selected_data = selected_data.loc[selected_data['neighborhood'] == neighborhood]
#         title_str += " in " + str(neighborhood)
#     if isSelected(street):
#         selected_data = selected_data.loc[selected_data['street'] == street]
#         title_str += " on " + street
#     if selected_data.empty:
#         title_str = "No matching data."

#     print("selected_data shape is : " + str(selected_data.shape))

#     weighted_mean = lambda x: np.average(x, weights=selected_data.loc[x.index, "count"])
#     function_dict = {'count': np.sum,
#                      'avg_land_value': weighted_mean,
#                      'avg_improvement_value': weighted_mean}
#     function_dict = {'count': np.sum}

#     grouped = selected_data.groupby(
#                     ["object_class"]).agg(function_dict).reset_index()
    grouped = selected_data.groupby('object_class').count().reset_index()
    print(grouped.columns)
    print(grouped.head(5))
    #grouped = selected_data.groupby(
    #                   ["use"]).agg(function_dict).reset_index()
    #print("grouped shape is : " + str(grouped.shape))
    #print(list(grouped))


    return create_pie_chart(grouped, title_str)

def isSelected(in_val):
    return not isinstance(in_val, list) and (in_val is not None)

if __name__ == '__main__':
#     app.run_server(debug=True) #if you run from local machine
     app.run_server(host="0.0.0.0") #from EC2 instance