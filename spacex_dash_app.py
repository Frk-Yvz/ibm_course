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

# Get the drop-down items
launch_list = spacex_df["Launch Site"].unique().tolist()
dropdown_list = [{'label': 'All Sites', 'value': 'ALL'}]
dropdown_list.extend([{'label': i, 'value': i} for i in launch_list])

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                      options=dropdown_list,
                                      placeholder="Select a Launch Site here",
                                      value="ALL",
                                      searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks = {0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        counts_0 = (filtered_df['class'] == 0).sum()
        counts_1 = (filtered_df['class'] == 1).sum()
        counts_list = [counts_1, counts_0]
        labels = ["Success", "Failure"]
        fig = px.pie(values=counts_list, labels=labels, names=[1,0], title="Total Success Launches for site {}".format(entered_site))
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_value):
    print('----------------------------------------------------------------')
    print(payload_value)
    print('-----------------------------------------------------------------')
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title='Correlation between Payload and Success for all Sites')
        fig.update_xaxes(range=[payload_value[0] - 300, payload_value[1] + 300])
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title='Correlation between Payload and Success for site {}'.format(entered_site))
        fig.update_xaxes(range=[payload_value[0] - 300, payload_value[1] + 300])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
