import dash
import pandas as pd
import altair as alt
import dash_core_components as dcc
import dash_html_components as html

# Importing Data
pd.read_csv('data/kaggle_survey_2020_responses.csv')

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])

app.layout = html.Div([
    # Slider values for years of experience
    html.Div([dcc.Slider(min = 0, max = 20, marks = {0 : '0', 20 : '20'})]),
    # Drop down for available roles
    html.Div([dcc.Dropdown(options = [
        {'label' : 'Data Scientist',
        'value' : 'Data Scientist'},
        {'label' : 'Software Engineeer',
        'value' : 'Software Engineer'}
    ])])])


if __name__ == '__main__':
    app.run_server(debug = True)