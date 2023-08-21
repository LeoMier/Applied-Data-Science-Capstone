import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update


app = dash.Dash(__name__)

spacex_df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv', 
                            encoding = "ISO-8859-1")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                html.Div(
                                    dcc.Dropdown(id='site-dropdown',
                                                 options=[
                                                     {'label': 'All Sites',     'value':'ALL'},
                                                     {'label': 'CCAFS LC-40',    'value': 'OPT1'},
                                                     {'label': 'VAFB SLC-4E',    'value': 'OPT2'},
                                                     {'label': 'KSC LC-39A',      'value': 'OPT3'},
                                                     {'label': 'CCAFS SLC-40',   'value': 'OPT4'}
                                                 ],
                                                 value='ALL',
                                                 placeholder='Select Launch Site',
                                                 searchable=True)
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='plot1')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                html.Div(
                                    dcc.RangeSlider(id='payload-slider',
                                                    min=0, max=10_000, step=1_000,
                                                    marks={i: i for i in range(0, 10_001, 2_500)},
                                                    value=[min_payload, max_payload])
                                ),

                                html.Div(dcc.Graph(id='plot2'))

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback([Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_pie_chart(chart: str, slider_values: list):
    
    if chart == 'ALL':
        pie = spacex_df.groupby(by='Launch Site')['class'].sum()
        pie_fig_all = px.pie(pie, values=pie.values, names=pie.index, title='Percentage of Successes by Site')

        spacex_df_1 =spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_values[0]) & (spacex_df['Payload Mass (kg)'] <= slider_values[1])]
        payload_fig = px.scatter(data_frame=spacex_df_1,
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version',
                            title='Correlation between Payload and Success for all Sites')

        return [pie_fig_all, payload_fig]
    
    if chart == 'OPT1':
        pie_1 = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40'].groupby(by='class')['Launch Site'].count()
        pie_fig_1 = px.pie(pie_1, values=pie_1.values, names=pie_1.index, title='CCAFS LC-40 Successful and Failed Missions')

        spacex_df_1 =spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_values[0]) & (spacex_df['Payload Mass (kg)'] <= slider_values[1]) & (spacex_df['Launch Site']=='CCAFS LC-40')]
        payload_fig = px.scatter(data_frame=spacex_df_1,
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version',
                            title='Correlation between Payload and Success for CCAFS LC-40')

        return [pie_fig_1, payload_fig]
    
    if chart == 'OPT2':
        pie_1 = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E'].groupby(by='class')['Launch Site'].count()
        pie_fig_1 = px.pie(pie_1, values=pie_1.values, names=pie_1.index, title='VAFB SLC-4E Successful and Failed Missions')

        spacex_df_1 =spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_values[0]) & (spacex_df['Payload Mass (kg)'] <= slider_values[1]) & (spacex_df['Launch Site']=='VAFB SLC-4E')]
        payload_fig = px.scatter(data_frame=spacex_df_1,
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version',
                            title='Correlation between Payload and Success for VAFB SLC-4E')

        return [pie_fig_1, payload_fig]

    if chart == 'OPT3':
        pie_1 = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A'].groupby(by='class')['Launch Site'].count()
        pie_fig_1 = px.pie(pie_1, values=pie_1.values, names=pie_1.index, title='KSC LC-39A Successful and Failed Missions')

        spacex_df_1 =spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_values[0]) & (spacex_df['Payload Mass (kg)'] <= slider_values[1]) & (spacex_df['Launch Site']=='KSC LC-39A')]
        payload_fig = px.scatter(data_frame=spacex_df_1,
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version',
                            title='Correlation between Payload and Success for KSC LC-39A')

        return [pie_fig_1, payload_fig]

    if chart == 'OPT4':
        pie_1 = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40'].groupby(by='class')['Launch Site'].count()
        pie_fig_1 = px.pie(pie_1, values=pie_1.values, names=pie_1.index, title='CCAFS SLC-40 Successful and Failed Missions')

        spacex_df_1 =spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_values[0]) & (spacex_df['Payload Mass (kg)'] <= slider_values[1]) & (spacex_df['Launch Site']=='CCAFS SLC-40')]
        payload_fig = px.scatter(data_frame=spacex_df_1,
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version',
                            title='Correlation between Payload and Success for CCAFS SLC-40')

        return [pie_fig_1, payload_fig]

    else:
        pie = spacex_df.groupby(by='Launch Site')['class'].sum()
        pie_fig_all = px.pie(pie, values=pie.values, names=pie.index, title='Percentage of Successes by Site')
        payload_fig = px.scatter(data_frame=spacex_df,
                        x='Payload Mass (kg)',
                        y='class',
                        color='Booster Version',
                        title='Correlation between Payload and Success for all Sites')
        return [pie_fig_all, payload_fig]
    
    


    

# Run the app
if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
    app.run_server(host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)