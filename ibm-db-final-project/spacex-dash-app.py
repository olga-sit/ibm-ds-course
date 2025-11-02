# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# TASK 1: Create a dropdown list for Launch Site selection
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
               [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart for total success counts
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter chart for payload vs. launch outcome
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df, 
            names='Launch Site', 
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        success_counts['class'] = success_counts['class'].replace({1: 'Success', 0: 'Failed'})
        fig = px.pie(
            success_counts,
            names='class',
            values='count',
            title=f'Total Success vs. Failed Launches for site {entered_site}'
        )
    return fig

# TASK 4: Callback for scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)

    if entered_site == 'ALL':
        filtered_df = spacex_df[mask]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & mask]

    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category',
        title='Payload vs. Launch Outcome'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8051)


