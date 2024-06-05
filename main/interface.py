import emoji  # type: ignore
import survey  # type: ignore
import sys

from data_proc.data_proc import tfl_modes, status_proc
from status_api.status import line_status, return_modes
from params import API_KEY

def main_app(modes: list):
    """
    Main application flow.

    Params:
        modes (list): A list of modes available for checking their status.

    Returns:
        bool: True if user wishes to continue, exits otherwise.
    """
    mode_idx = survey.routines.select('Please select a TFL service: ', options=modes)
    chosen_mode = modes[mode_idx]
    line_data = line_status(app_key=API_KEY, modes=chosen_mode)

    service_dict = status_proc(line_data, is_tube=(chosen_mode == 'Tube'))
    status_codes = service_dict['status_code']

    if chosen_mode == 'Overground':
        if service_dict['status_code'][0] == 10:
            print(f"\nThere is {service_dict['status'][0]} on the {chosen_mode}\n")
        else:
            reason = service_dict['reason'][0]
            print('Bad luck, friend!')
            print(emoji.emojize(f"The current status of the {chosen_mode} is: :sparkles: {service_dict['status'][0]} :sparkles:"))
            print(f'The reason is:\n{reason.strip()}')

    elif chosen_mode == 'Tube':
        if 10 in set(status_codes) and len(set(status_codes)) == 1:
            print(f"\nThere is good service for all lines on the {chosen_mode}\n")
        else:
            for idx, status_code in enumerate(status_codes):
                if status_code != 10:
                    reason = service_dict['reason'][idx]
                    print(emoji.emojize(f"The current status of the {service_dict['line'][idx]} is: :sparkles: {service_dict['status'][idx]} :sparkles:"))
                    print(f'The reason is:\n{reason.strip()}')

    continue_idx = survey.routines.select('Would you like to check another service?', options=['Yes', 'No'])
    if continue_idx == 0:
        return True
    print('\nGoodbye!')
    sys.exit(0)

def run_app():
    """
    Runs the main application loop.
    """
    modes = [mode for mode in tfl_modes(return_modes(app_key=API_KEY)) if mode.lower() in ['tube', 'overground']]

    try:
        while True:
            main_app(modes)
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
