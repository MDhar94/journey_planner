import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import emoji
from status_api.status import line_status, return_modes
from data_proc.data_proc import issue_reason, tfl_modes, status_proc
from params import API_KEY

# Initialize the Dash app
app = dash.Dash(__name__)

# Fetch initial data
modes_data = return_modes(app_key=API_KEY)
modes = tfl_modes(modes_data)
filtered_modes = [mode for mode in modes if mode.lower() in ['tube', 'overground']]

app.layout = html.Div([
    html.H1("Transport Service Status Checker"),
    html.Button('Check Tube and Overground Status', id='status-btn', n_clicks=0),
    html.Div(id='status-output')
])

# Helper function to fetch and format status
def get_status(mode):
    line_data = line_status(app_key=API_KEY, modes=mode)
    status, status_code = status_proc(line_data)
    if status_code == 10:
        return html.P(f"There is {status} on the {mode}")
    else:
        reason = issue_reason(line_data).split(':')[1]
        return html.Div([
            html.P("Bad luck, friend!"),
            html.P(f"The {mode} is experiencing a {emoji.emojize(':sparkles:')} {status} {emoji.emojize(':sparkles:')}"),
            html.P("The reason is:"),
            html.P(reason.strip())
        ])

# Callback to update the status
@app.callback(
    Output('status-output', 'children'),
    Input('status-btn', 'n_clicks')
)
def update_status(n_clicks):
    if n_clicks > 0:
        statuses = []
        for mode in filtered_modes:
            status = get_status(mode)
            statuses.append(status)
        return statuses

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
