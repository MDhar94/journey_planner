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
    dcc.Dropdown(
        id='mode-selector',
        options=[{'label': mode, 'value': mode} for mode in filtered_modes],
        placeholder="Select a TFL service"
    ),
    html.Button('Check Status', id='status-btn', n_clicks=0),
    html.Div(id='status-output')
])

@app.callback(
    Output('status-output', 'children'),
    Input('status-btn', 'n_clicks'),
    [Input('mode-selector', 'value')]
)
def update_status(n_clicks, selected_mode):
    if n_clicks > 0 and selected_mode:
        line_data = line_status(app_key=API_KEY, modes=selected_mode)
        status, status_code = status_proc(line_data)
        if status_code == 10:
            return f"There is {status} on the {selected_mode}"
        else:
            reason = issue_reason(line_data).split(':')[1]
            return [html.P("Bad luck, friend!"),
                    html.P(f"The {selected_mode} is experiencing a {emoji.emojize(':sparkles:')} {status} {emoji.emojize(':sparkles:')}"),
                    html.P("The reason is:"),
                    html.P(reason.strip())]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
