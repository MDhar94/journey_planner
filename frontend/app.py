import dash
from dash import html
from dash.dependencies import Input, Output
import emoji
from status_api.status import line_status, return_modes
from data_proc.data_proc import issue_reason, tfl_modes, status_proc
from params import API_KEY

app = dash.Dash(__name__
                , assets_folder='./static')

# Get data
modes_data = return_modes(app_key=API_KEY)
modes = tfl_modes(modes_data)
filtered_modes = [mode for mode in modes if mode.lower() in ['tube', 'overground']]

# App layout with CSS classes
app.layout = html.Div([
    html.H1("TFL Status Checker", className='header')
    , html.Div([
        html.Button('Check Tube and Overground', id='status-btn', n_clicks=0, className='button')
    ]
              , className='flex-center')
    , html.Div(id='status-output', className='status-output')
    ]
                      , className='container')

def get_status(mode):
    line_data = line_status(app_key=API_KEY, modes=mode)
    status, status_code = status_proc(line_data)
    if status_code == 10:
        return html.P(f"There is {status} on the {mode.lower()} {emoji.emojize(':check_mark_button:')}"
                      , style={'color': '#007849'})
    else:
        reason = issue_reason(line_data).split(':')[1]
        return html.Div([
            html.P("Bad luck, friend!"
                   , style={'color': '#EE3224'}),
            html.P(f"The {mode} is experiencing a {emoji.emojize(':sparkles:')} {status} {emoji.emojize(':sparkles:')}"
                   , style={'fontWeight': 'bold'}),
            html.P("The reason is:"
                   , style={'color': '#003688'}),
            html.P(reason.strip()
                   , style={'marginLeft': '20px'})
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
