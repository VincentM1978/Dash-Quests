import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px

###################################################### importation et nettoyage du csv #########################################################


df = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', sep=',', on_bad_lines='skip', low_memory=False)
df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
df['year'] = df['publication_date'].dt.year
df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
df['year'] = df['year'].astype(float).astype(pd.Int64Dtype())


###################################################### creation de l'application #########################################################

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

############################################################# creation du layout #############################################################

# Define the layout of the app
app.layout = html.Div([
    html.H1("Book Dataset Analysis"),
    
    # Dropdown for variable 1
    dcc.Dropdown(
        id='variable1',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='average_rating',
        clearable=False
    ),
    
    # Dropdown for variable 2
    dcc.Dropdown(
        id='variable2',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='num_pages',
        clearable=False
    ),
    
    # Graph
    dcc.Graph(id='plot'),
])


###################################################### creation des callbacks #########################################################

# Define the callback to update the plot
@app.callback(
    dash.dependencies.Output('plot', 'figure'),
    dash.dependencies.Input('variable1', 'value'),
    dash.dependencies.Input('variable2', 'value')
)
def update_plot(variable1, variable2):
    fig = px.scatter(df, x=variable1, y=variable2, hover_data=['title'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
