import dash
import dash_html_components as html
import dash_core_components as dcc #Interativity Components
import dash_bootstrap_components as dbc #layout component
from dash.dependencies import Input, Output
# import numpy as np
import pandas as pd
import altair as alt



kaggle_survey = pd.read_csv(r'data/Processed/general_processed_data.csv')
languages_barplot_data =  pd.read_csv(r'data/Processed/lang_barplot_data.csv')
ml_barplot_data = pd.read_csv(r'data/Processed/ml_barplot_data.csv')
fluctuation_plot_data = pd.read_csv(r'data/Processed/Fluctuation_plot_data.csv')

def slider_recognition(prog_exp__val):
    if prog_exp__val == 0:
        exp_range = '< 1 years'
    elif prog_exp__val == 1:
        exp_range = '1-2 years'
    elif prog_exp__val == 2:
        exp_range = '3-5 years'
    elif prog_exp__val == 3:
        exp_range = '5-10 years'
    elif prog_exp__val == 4:
        exp_range = '10-20 years'
    else:
        exp_range = '20+ years'
    return(exp_range)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container([
    
    html.H1("Data Science Decision Aid Dashboard", style={'color' : '#D6ED17FF', 'background-color' : '#606060FF'}),
    #html.Br(),
    html.P("This dashboard has the objective of informing Data Science students,\
             professional and even prospects (future data science professionals) the worldwide state of the art regarding most used programming languages,\
             machine learning methods, the recommended programs to learn first with a considerable aggregated value(for prospects) and yearly income of different job titles.",
             style={'color' : '#D6ED17FF', 'background-color' : '#606060FF'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
           html.Label(["Programming Experience", dcc.Slider(id='slider',min=0, max=5, marks = {0 : '<1 years', 1 : '1-2 years', 2 : '3-5 years',
                3 : '5-10 years', 4 : '10-20 years', 5 : '+20 years'})], style={'height': '50px', 'width': '500px'})
             ],md=6),
        html.Br(),
        dbc.Col([
           html.Label(["Job Title", dcc.Dropdown(id = 'job_title_val', placeholder='Enter a Job Title', value='Data Scientist', options = [
        {'label' : 'Data Scientist','value' : 'Data Scientist'},
        {'label' : 'Software Engineeer','value' : 'Software Engineer'},
        {'label' : 'Data Analyst','value' : 'Data Analyst'},
        {'label' : 'Machine Learning Engineer','value' : 'Machine Learning Engineer'},
        {'label' : 'Business Analyst','value' : 'Business Analyst'},
        {'label' : 'Product/Project Manager','value' : 'Product/Project Manager'},
        {'label' : 'Data Engineer','value' : 'Data Engineer'},
        {'label' : 'Statistician','value' : 'Statistician'},
        {'label' : 'DBA/Database Engineer','value' : 'DBA/Database Engineer'}], style={'height': '50px', 'width': '500px'})])
             ])
    ]),
    
    #html.Br(),
    dbc.Row([
        dbc.Col([html.Iframe(id="lang_bar",style={'border-width': '0', 'width': '300%', 'height': '350px'})], md=6),
        dbc.Col([html.Iframe(id ="ml_bar",style={'border-width': '0', 'width': '300%', 'height': '350px'})])
       ]),

    html.Br(),
    dbc.Row([
        dbc.Col([dbc.Row([html.Label(["Median Salary - Lowest Range:", dbc.Card(dbc.CardBody(id='median_salary_l'), style={'text-align': 'center', 'width': '200%'}, color='warning')])]), 
        dbc.Row([html.Label(["Median Salary - Highest Range:", dbc.Card(dbc.CardBody(id='median_salary_h'), style={'text-align': 'center', 'width': '198%'}, color='warning')])])], md=6),
        #html.Br(),
        dbc.Col([html.Iframe(id="fluct_points", style={'border-width': '0', 'width': '600%', 'height': '600px'})], md=6)
       ])])

    #dbc.Row([
        #dbc.Col([html.Label(["Median Salary - Lowest Range:", html.Div(id='median_salary_l', style={'color' : 'blue'})]), 
        #html.Label(["Median Salary - Highest Range:", html.Div(id='median_salary_h', style={'color' : 'blue'})])], md=6),
        #html.Br(),
        #dbc.Col([html.Iframe(id="fluct_points",style={'border-width': '0', 'width': '600%', 'height': '600px'})], md=6)
       #])])
    
    #dcc.Textarea(id='widget-2'),
    #html.Iframe(id="fluct_points",style={'border-width': '0', 'width': '600%', 'height': '600px'})])




@app.callback(
    Output('lang_bar', 'srcDoc'),
    Input('job_title_val', 'value'),
    Input('slider', 'value'))
def plot_languages_barplot(job, prog_exp__val):
    exp_range = slider_recognition(prog_exp__val)
    lang_barplot = alt.Chart(languages_barplot_data.query("Q5 == @job & Q6 == @exp_range"), 
            title = "Most Used Programming Languages").mark_bar().encode(
        alt.Y("selected_lang", title="Programming Languages", sort="-x"),
        alt.X("count()"),
        alt.Tooltip("count()")).interactive()
    return lang_barplot.to_html()

@app.callback(
    Output('ml_bar', 'srcDoc'),
    Input('job_title_val', 'value'),
    Input('slider', 'value'))
def plot_ml_barplot(job, prog_exp__val):
    exp_range = slider_recognition(prog_exp__val)
    ml_barplot = alt.Chart(ml_barplot_data.query("Q5 == @job & Q6 == @exp_range"), 
            title = "Most Used Machine Learning Methods").mark_bar().encode(
        alt.Y("selected_ml_method",title="ML Methods", sort="-x"),
        alt.X("count()"),
        alt.Tooltip("count()")).interactive()#.properties(width=300)
    return ml_barplot.to_html()

@app.callback(
    Output('fluct_points', 'srcDoc'),
    Input('job_title_val', 'value'),
    Input('slider', 'value'))
def plot_funct_plot(job, prog_exp__val):
    exp_range = slider_recognition(prog_exp__val)
    fluct_plot = alt.Chart(fluctuation_plot_data.query("Q5 == @job & Q6 == @exp_range"),
    title = "Relationship between Level of Education and Recommended Programs").mark_point().encode(
        alt.Y("Q4", title = "Current Level of Education"),
        alt.X("Q8", title = "Recommended Languages to Learn"),
        alt.Color("count()"),
        alt.Size("count()",title = "Counts", scale = alt.Scale(range = (60, 250)))).properties(height=250, width=320)
    return fluct_plot.to_html()

@app.callback(
    Output('median_salary_l', 'children'),
    Input('job_title_val', 'value'),
    Input('slider', 'value'))
def calculate_salary(job, prog_exp__val):
    exp_range = slider_recognition(prog_exp__val)
    data = kaggle_survey.query("Q5 == @job & Q6 == @exp_range")
    return str(data["lower"].median()) + " (USD)"

@app.callback(
    Output('median_salary_h', 'children'),
    Input('job_title_val', 'value'),
    Input('slider', 'value'))
def calculate_salary(job, prog_exp__val):
    exp_range = slider_recognition(prog_exp__val)
    data = kaggle_survey.query("Q5 == @job & Q6 == @exp_range")
    return str(data["higher"].median()) + " (USD)"


if __name__ == '__main__':
    app.run_server(debug=True)