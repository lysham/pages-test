from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


def process_csv(file):
    df = pd.read_csv(file)
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    df['date'] = df['TIMESTAMP'].dt.date.astype('str')
    return df


global data
data = process_csv('NCH_01.csv')

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(['Last 24 Hours', 'Last 2 Days', 'Last 5 Days', 'Last 7 Days'],
                 'Last 24 Hours', id='plot_duration'),
    html.Div(id='scatter_plot')
])


@app.callback(
    Output('scatter_plot', 'children'),
    Input('plot_duration', 'value')
)
def update_output(value):
    if value == 'Last 24 Hours':
        n_day = 1
    else:
        n_day = [int(i) for i in value.split() if i.isdigit()][0]

    dates = data.date.unique()[-n_day:]
    dff = data[data['date'].isin(dates)]
    plot1 = px.scatter(dff, x='TIMESTAMP',
                       y=['RSR_GHI_Avg', 'PSP_GHI_Avg', 'SPN_GHI_Avg'],
                       title='GHI vs. Time')

    return [dcc.Graph(id='GHI_scatter', figure=plot1)]


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)