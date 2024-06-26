# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                    value='ALL',  # default value
                                    placeholder='Select a Launch Site',
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                    value=[min_payload, max_payload],
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def generate_success_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, names='class', color = 'class', color_discrete_map={1: 'green', 0: 'red'}, 
        title='Total Success Launches by Class')
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(site_df, names='class', color = 'class', color_discrete_map={1: 'green', 0: 'red'}, 
        title='Total Success Launches by Class')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def generate_success_payload_scatter_chart(site, payload_range):
    if site == 'ALL':
        site_df = spacex_df
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == site]

    filtered_df = site_df[(site_df['Payload Mass (kg)'] >= payload_range[0]) & (site_df['Payload Mass (kg)'] <= payload_range[1])]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                        title='Correlation between Payload and Launch Success', 
                        category_orders={'class': ['0', '1']})
    fig.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=['Failure', 'Success']))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(use_reloader=True)
