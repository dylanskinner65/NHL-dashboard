
# Import necessary modules
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
import json
import numpy as np

# Team colors
nhl_teams_colors = {
    'Anaheim Ducks': '#f47a38',
    'Arizona Coyotes': '#8c2633',
    'Atlanta Flames': '#e03a3e',
    'Atlanta Thrashers': '#00214e',
    'Boston Bruins': '#fcb514',
    'Brooklyn Americans': '#002f87',
    'Buffalo Sabres': '#002654',
    'California Golden Seals': '#fdba31',
    'Calgary Flames': '#c8102e',
    'California/Oakland (Golden) Seals': '#fdba31',
    'Carolina Hurricanes': '#cc0000',
    'Chicago Blackhawks': '#cf0a2c',
    'Cleveland Barons': '#ce0f69',
    'Colorado Avalanche': '#6f263d',
    'Colorado Rockies': '#8c2633',
    'Columbus Blue Jackets': '#00285c',
    'Dallas Stars': '#006847',
    'Detroit Cougars': '#ce1126',
    'Detroit Falcons': '#ce1126',
    'Detroit Red Wings': '#ce1126',
    'Edmonton Oilers': '#c8102e',
    'Florida Panthers': '#041e42',
    'Hamilton Tigers': '#ce1126',
    'Hartford Whalers': '#007a33',
    'Kansas City Scouts': '#ce0f69',
    'Los Angeles Kings': '#a2aaad',
    'Minnesota North Stars': '#154734',
    'Minnesota Wild': '#154734',
    'Montréal Canadiens': '#af1e2d',
    'Montréal Maroons': '#af1e2d',
    'Montréal Wanderers': '#af1e2d',
    'Nashville Predators': '#ffb81c',
    'New England Whalers': '#007a33',
    'New Jersey Devils': '#ce1126',
    'New York Americans': '#002f87',
    'New York Islanders': '#f47d30',
    'New York Rangers': '#0038a8',
    'Oakland Seals': '#fdba31',
    'Ottawa Senators (original)': '#e4173e',
    'Ottawa Senators': '#c52032',
    'Philadelphia Flyers': '#f74902',
    'Phoenix Coyotes': '#8c2633',
    'Pittsburgh Pirates': '#000000',
    'Pittsburgh Penguins': '#000000',
    'Québec Nordiques': '#1b4f72',
    'San Diego Gulls': '#fdba31',
    'San Francisco Seals': '#fdba31',
    'San Jose Sharks': '#006d75',
    'Seattle Kraken': '#82b3be',
    'St. Louis Blues': '#002f87',
    'Tampa Bay Lightning': '#002868',
    'Toronto Arenas': '#003e7e',
    'Toronto Maple Leafs': '#003e7e',
    'Vancouver Canucks': '#001f5b',
    'Vegas Golden Knights': '#b4975a',
    'Victoria Cougars': '#ce1126',
    'Washington Capitals': '#041e42',
    'Winnipeg Jets': '#041e42'
}

# Read in JSON file
df = pd.read_json("2022-23.json")

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout for the app
app.layout = html.Div(children=[
    # Create a row to hold the two columns
    html.Div([
        # First column (graph)
        html.Div([
            # Add a title to the graph
            html.H1(children='Points Progression by Team'),
            # Add the graph component to the first column
            dcc.Graph(id='graph')
        ], className='eight columns'),  # Use the "eight columns" class to make this column take up 8/12 of the row
        
        # Second column (dropdown menu)
        html.Div([
            # Create the dropdown menu
            dcc.Dropdown(
                id='year-dropdown',  # Give the dropdown menu an ID so we can reference it in the callback function
                options=[{'label': team, 'value': team} for team in df.columns.tolist()],  # Set the options for the dropdown menu to the years in the dataframe
                value=df.columns.to_list()[0],  # Set the default value of the dropdown menu to the first year in the dataframe
                multi=True
            )
        ], className='four columns')  # Use the "four columns" class to make this column take up 4/12 of the row
    ], className='row'),  # Use the "row" class to create a row
    
])

# Define the callback function that updates the graph based on the dropdown menu value
@app.callback(
    dash.dependencies.Output('graph', 'figure'),  # Output the updated graph to the 'graph' component
    [dash.dependencies.Input('year-dropdown', 'value')]  # Get the value of the dropdown menu
)
def update_figure(selected_year):
    # Filter the dataframe to only include data for the selected year
    filtered_df = df[selected_year]
    
    # Create a subplot figure with two columns
    fig = make_subplots(rows=1, cols=1, subplot_titles="Season Points", x_title="Games Played", y_title="Points")

    # See if we have one team selected, or multiple
    if type(selected_year) == str:  # This means there is only one team
        selected_year = [selected_year]
    
    # Add a trace for sales to the first column of the subplot figure
    for team in selected_year:
        fig.add_trace(
            go.Scatter(x=filtered_df[team]['Games'], y=filtered_df[team]['Points'], mode='lines', name=team, line_color=nhl_teams_colors[team]),
            row=1, col=1,
        )

    
    # Update the layout of the subplot figure
    fig.update_layout(height=500, width=1000)
    
    # Return the updated subplot figure
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

