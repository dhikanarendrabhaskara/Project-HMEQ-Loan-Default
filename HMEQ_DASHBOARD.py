import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
from dash.dependencies import Input, Output, State
import pickle
import numpy as np
import dash_table

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size)

data = pd.read_csv('mydata.csv')
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
loadModel = pickle.load(open('hmeq_loan_default_tuned.sav', 'rb'))

app.layout = html.Div(children=[
    html.H1('HOME EQUITY LOAN'),
    html.Div(children='by Dhika Narendra Bhaskara'),

    dcc.Tabs(children=[
        dcc.Tab(value='Tab1', label='DataFrames',children=[
            html.Div([
                html.Div(children=[
                    html.P('Reason: '),
                    dcc.Dropdown(id='filter-reason', value = 'None',
                    options= [{'label' : 'None', 'value' : 'None'},
                              {'label' : 'Home Improvement', 'value' : 'HomeImp'},
                              {'label' : 'Debt Consolidation', 'value' : 'DebtCon'},
                              ])
                ], className='col-3'),

                html.Div(children=[
                    html.P('Job: '),
                    dcc.Dropdown(id='filter-job', value = 'None',
                    options= [{'label' : 'None', 'value' : 'None'},
                              {'label' : 'Other', 'value' : 'Other'},
                              {'label' : 'Office', 'value' : 'Office'},
                              {'label' : 'Manager', 'value' : 'Mgr'},
                              {'label' : 'ProfExe', 'value' : 'ProfExe'},
                              {'label' : 'Self', 'value' : 'Self'},
                              {'label' : 'Sales', 'value' : 'Sales'},
                              ]),
                ], className='col-3'),

                html.Div(children=[
                    html.P('Default : '),
                    dcc.Dropdown(id='filter-default', value = 'None',
                    options= [{'label' : 'None', 'value' : 'None'},
                              {'label' : 'Yes', 'value' : 1 },
                              {'label' : 'No', 'value' : 0 },
                              ])
                ], className='col-3'),
            ], className='row'),
            
            html.Br(),
            html.Div([
                html.P('Max Rows: '),
                dcc.Input(id ='filter-row',
                            type = 'number', 
                            value = 10)
                ], className = 'row col-3'),
            
            html.Div(children=[
                html.Button('search', id = 'filter')
                ],className = 'row col-4'),
                            
            html.Div(id='div-table',
                children=[generate_table(data)])
        ]),

        dcc.Tab(value='Tab2', label='Plots & Graphs',children=[
            html.Div([
                dcc.Graph(
                id='Graph1',
                figure ={
                'data':[
                    {'x': data['JOB'],'y': data['LOAN'], 'type': 'violin', 'name':'violinplot' },
                    {'x': data['JOB'],'y': data['LOAN'], 'type': 'box', 'name':'boxplot' }
                    
                ],
                'layout': {'title': 'Job Category & Loan Amount'}
            })
            ], className = 'col-12'),

            html.Div(children = dcc.Graph(
                id = 'Graph2',
                figure = {'data':[
                go.Pie(
                    labels = data['REASON'].unique(),
                    values = [data[data['REASON']=='HomeImp']['LOAN'].mean(),
                    data[data['REASON']=='DebtCon']['LOAN'].mean()], textinfo='label+percent')            
                ],
                'layout':go.Layout(
                    title='Loan Reason & Loan Amount Average', hovermode = 'closest')
            }
            ), className = 'col-12'),
  
            html.Div(children = dcc.Graph(
                id = 'Graph3',
                figure = {'data':[
                go.Scatter(
                    x=data[data['BAD']==i]['LOAN'],
                    y=data[data['BAD']==i]['DELINQ'],
                    mode='markers',
                    name='Default {}'.format(i)
                    ) for i in data['BAD'].unique()            
                ],
                'layout':go.Layout(
                    xaxis={'title':'Loan Amount'},
                    yaxis={'title':'Delinquent Credits'},
                    title='Delinquent Credit Lines & Loan Amount',
                    hovermode='closest'
                )
            }   
            ), className = 'col-11'), 
        ]),

        dcc.Tab(value='Tab3', label='Default Predictions', children=[
            html.Div([
                html.Div(children=[
                    html.P('Reason for loan: '),
                    dcc.Dropdown(id='my-id-reason', value = 'HomeImp',
                    options= [{'label' : 'Home Improvement', 'value' : 'HomeImp'},
                            {'label' : 'Debt Consolidation', 'value' : 'DebtCon'}])
                ], className='col-3'),

                html.Div(children=[
                    html.P('Job: '),
                    dcc.Dropdown(id='my-id-job', value = 'Other',
                    options= [{'label' : 'Other', 'value' : 'Other'},
                            {'label' : 'Office', 'value' : 'Office'},
                            {'label' : 'Manager', 'value' : 'Mgr'},
                            {'label' : 'ProfExe', 'value' : 'ProfExe'},
                            {'label' : 'Self', 'value' : 'Self'},
                            {'label' : 'Sales', 'value' : 'Sales'}]),
                ], className='col-3'),
            ], className='row'),

            html.Br(),
            html.Div([
                html.Div([
                    html.P('Loan requested: '),
                    dcc.Input(id='my-id-loan', value = '0', type = 'number')
                ], className='col-3'),

                html.Div(children=[
                    html.P('Mortgage due amount: '),
                    dcc.Input(id='my-id-mortdue', value = '0', type = 'number')
                ], className='col-3'),

                html.Div(children=[
                    html.P('Current property value: '),
                    dcc.Input(id='my-id-value', value = '0', type = 'number')
                ], className='col-3'),

                html.Div(children=[
                    html.P('Total credit lines: '),
                    dcc.Input(id='my-id-clno', value = '0', type = 'number'),
                ], className='col-3')
            ], className='row'),

            html.Br(),
            html.Div([
                html.Div(children=[
                    html.P('Recent credit lines: '),
                    dcc.Input(id='my-id-ninq', value = '0', type = 'number'),
                ], className='col-3'),

                html.Div(children=[
                    html.P('Years on the job: '),
                    dcc.Input(id='my-id-yoj', value = '0', type = 'number'),
                ], className='col-3'),

                html.Div(children=[
                    html.P('Delinquent credit lines: '),
                    dcc.Input(id='my-id-delinq', value = '0', type = 'number'),
                ], className='col-3'),

                html.Div(children=[
                    html.P('Oldest credit line (months): '),
                    dcc.Input(id='my-id-clage', value = '0', type = 'number'),
                ], className='col-3')
            ], className='row'),
        
            html.Br(),
            html.Div(id = 'my-div')
        ])#dcc.Tab
        

    ], content_style= {
            'fontFamily': 'Arial',
            'borderBottom': '1px solid #d6d6d6',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'padding': '44px'
        }
    )#dcc.Tabs
      
    ]#children(app_layout)
)#app_layout

@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'),
    State(component_id = 'filter-reason', component_property = 'value'),
    State(component_id = 'filter-job', component_property = 'value'),
    State(component_id = 'filter-default', component_property = 'value')]
)

def update_table(n_clicks, row, reason, job, default):
    data = pd.read_csv('mydata.csv')
    if reason != 'None':
        data = data[data['REASON'] == reason]
    if job != 'None':
        data = data[data['JOB'] == job]
    if default != 'None':
        data = data[data['BAD'] == default]
    children = [generate_table(data, page_size = row)]
    return children

@app.callback(
    Output('my-div', 'children'),
    [Input('my-id-loan', 'value'),
     Input('my-id-mortdue', 'value'),
     Input('my-id-value', 'value'),
     Input('my-id-reason', 'value'),
     Input('my-id-job', 'value'),
     Input('my-id-yoj', 'value'),
     Input('my-id-delinq', 'value'),
     Input('my-id-clage', 'value'),
     Input('my-id-ninq', 'value'),
     Input('my-id-clno', 'value')]     
)

def update_output_div(my_id_loan, my_id_mortdue, my_id_value, my_id_reason, my_id_job, my_id_yoj, my_id_delinq, my_id_clage, my_id_ninq, my_id_clno):
    my_loan = my_id_loan 
    my_mortdue = my_id_mortdue
    my_value = my_id_value
    
    my_reason = 0
    if(my_id_reason == 'HomeImp'):
        my_reason = 1

    my_job_of = 0
    my_job_ot = 0
    my_job_pr = 0
    my_job_sa = 0
    my_job_se = 0
    if(my_id_job == 'Office'):
        my_job_of = 1
    elif(my_id_job == 'Other'):
        my_job_ot = 1
    elif(my_id_job == 'ProfExe'):
        my_job_pr = 1
    elif(my_id_job == 'Sales'):
        my_job_sa = 1
    elif(my_id_job == 'Self'):
        my_job_se = 1

    my_yoj = my_id_yoj
    my_delinq = my_id_delinq
    my_clage = my_id_clage
    my_ninq = my_id_ninq
    my_clno = my_id_clno

    data_baru = pd.DataFrame(data = [(my_loan, my_mortdue, my_value, my_yoj, my_delinq,
            my_clage, my_ninq, my_clno, my_reason, my_job_of, my_job_ot, my_job_pr,
            my_job_sa, my_job_se)], 
            columns = ['LOAN', 'MORTDUE', 'VALUE', 'YOJ', 'DELINQ', 'CLAGE', 'NINQ',
            'CLNO', 'REASON_HomeImp', 'JOB_Office', 'JOB_Other', 'JOB_ProfExe',
            'JOB_Sales', 'JOB_Self'])

    predict = loadModel.predict(data_baru)
    if predict == 1: 
        return "\nOutput: If not careful, you could default"
    if predict == 0:
        return "\nOutput: Be careful & you'll be fine"
        

if __name__ == '__main__':
    app.run_server(debug=True)