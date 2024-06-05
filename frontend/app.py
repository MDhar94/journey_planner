# Look into hosting on app engine (GCP)

import dash
from dash import html
from dash.dependencies import Input, Output
import emoji
from status_api.status import line_status, return_modes
from data_proc.data_proc import tfl_modes, status_proc
from params import API_KEY

app = dash.Dash(__name__
                , assets_folder='./static')

# Get data
modes_data = return_modes(app_key=API_KEY)
modes = tfl_modes(modes_data)
filtered_modes = [mode.lower() for mode in modes if mode.lower() in ['overground','tube']]

# App layout with CSS classes
app.layout = html.Div([
    html.H1("TFL Status Checker", className='header'),
    html.Div([
        html.Button('Check Tube and Overground', id='status-btn', n_clicks=0, className='button'),
    ], className='flex-center'),
    html.Div(id='service-message', className='service-message'),
    html.Div(id='tube-status-output', className='status-output'),
    html.Div(id='overground-status-output', className='status-output')
], className='container')

def get_status(mode):

    service_dict = status_proc(line_status(app_key=API_KEY, modes=mode), is_tube=(mode == 'tube'))

    if mode == 'overground':

        status_code = service_dict['status_code'][0]
        status = service_dict['status'][0]
        reason = service_dict['reason'][0]

        if status_code == 10:

            return html.P(f"There is {status.lower()} on the {mode} {emoji.emojize(':check_mark_button:')}"
                          , style={'color': '#007849'})

        else:

            return html.Div([
                html.P("Bad luck, friend!"
                    , style={'color': '#EE3224'}),
                html.P(f"The status of the {mode} is: {emoji.emojize(':sparkles:')} {status} {emoji.emojize(':sparkles:')}"
                    , style={'fontWeight': 'bold'}),
                html.P("Affected segment & reason:"
                    , style={'color': '#003688'}),
                html.P(reason.strip()
                    , style={'marginLeft': '20px'})
            ])

    if mode == 'tube':

        status_codes = service_dict['status_code']

        if 10 in set(status_codes) and len(set(status_codes)) == 1:

            return html.P(f"There is good service for all lines on the {mode} {emoji.emojize(':check_mark_button:')}"
                          , style={'color': '#007849'})

        else:

            tube_children = []

            status_codes = service_dict['status_code']
            statuses = service_dict['status']
            reasons = service_dict['reason']
            line_names = service_dict['line_name']

            for idx, status_code in enumerate(status_codes):
                if status_code != 10:

                    tube_children.append(
                        html.P(f"The status of the {line_names[idx]} is: {emoji.emojize(':sparkles:')} {statuses[idx]} {emoji.emojize(':sparkles:')}"
                               , style={'fontWeight': 'bold'}))
                    tube_children.append(
                        html.P("Affected segment & reason:"
                               , style={'color': '#003688'}))
                    tube_children.append(
                        html.P(reasons[idx].strip()
                               , style={'marginLeft': '20px'}))

            return html.Div(tube_children)

@app.callback(
    [Output('tube-status-output', 'children')
     , Output('overground-status-output', 'children')
     , Output('service-message', 'children')],
    [Input('status-btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_output(n_clicks):
    if n_clicks > 0:
        tube_status = get_status('tube')
        overground_status = get_status('overground')
        # Check if any status is not 'Good Service' and display a message

        message = 'Sorry, friend!' if 'good' not in str(tube_status) or 'good' not in str(overground_status) else ''
        return tube_status, overground_status, message
    return '', '', ''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
