import dash
from dash_html_components.Div import Div
import pandas as pd
import altair as alt
import dash_core_components as dcc
import dash_html_components as html

# Importing Data
kaggle_survey = pd.read_csv('MDS/532/career_deciscion_aid/data/kaggle_survey_2020_responses.csv',
 skiprows=[1])

language_columns = kaggle_survey.filter(regex = 'Q7', axis =1).columns.to_list()
kaggle_langs = kaggle_survey.melt(
    id_vars = 'Q5', value_vars = language_columns, value_name = 'prog_lang').dropna()

alt.data_transformers.disable_max_rows()

lang_chart = alt.Chart(data = kaggle_langs).mark_bar().encode(
    x = 'prog_lang',
    y = 'count()')

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])

app.layout = html.Div([
    # Slider values for years of experience
    html.Div([dcc.Slider(min = 0, max = 20, marks = {0 : '0', 20 : '20'})]),
    # Drop down for available roles
    html.Div([dcc.Dropdown(options = [
        {'label' : 'Data Scientist',
        'value' : 'Data Scientist'},
        {'label' : 'Software Engineeer',
        'value' : 'Software Engineer'}])]),
    # Language Chart
    html.Div(html.Iframe(srcDoc = lang_chart.to_html(), style = {
        'border-width' : '0',
        'width' : '100%',
        'height' : '400px'}))
    ])


if __name__ == '__main__':
    app.run_server(debug = True)