import emoji # type: ignore
import survey # type: ignore
import sys

from data_proc.data_proc import issue_reason, issue_reason_tube, tfl_modes, status_proc, status_proc_tube
from status_api.status import line_status, return_modes
from params import API_KEY

def main_app(modes):

    """The main flow of this app"""

    mode_idx = survey.routines.select('Please select a TFL service: '
                                   , options = modes)

    chosen_mode = modes[mode_idx]

    line_data = line_status(app_key=API_KEY, modes=chosen_mode)

    if chosen_mode == 'Overground':

        status, status_code = status_proc(line_data)

        if status_code == 10:
            print(f"\nThere is {status} on the {chosen_mode}\n")

        else:
            reason = issue_reason(line_data).split(':')[1]
            print('Bad luck, friend!')
            print(emoji.emojize(f"The {chosen_mode} is experiencing a :sparkles: {status} :sparkles:"))
            print(f'The reason is:')
            print(reason.strip())

    else:

        tube_line_data = status_proc_tube(line_data)

        status_codes = tube_line_data['status_code']

        if 10 in set(status_codes) and len(set(status_codes)) == 1:

            print(f"\nThere is good service for all lines on the {chosen_mode}\n")

        else:

            for idx, status_code in enumerate(status_codes):

                if status_code != 10:
                    print(emoji.emojize(f"The {tube_line_data['line'][idx]} is experiencing :sparkles: {tube_line_data['status'][idx]} :sparkles:"))
                    reason = issue_reason_tube(line_data[idx]).split(':')[1]
                    print(f"The reason is:")
                    print(reason.strip())

    continue_idx = survey.routines.select('Would you like to check another service?'
                                          , options = ['Yes','No'])

    if continue_idx == 0:
        return True
    print('\nGoodbye!')
    sys.exit(0)

def run_app():

    modes_data = return_modes(app_key=API_KEY)
    modes = tfl_modes(modes_data)

    modes = [mode for mode in modes if mode.lower() in ['tube','overground']]

    try:
        while True:
            main_app(modes)
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)

if __name__ == "__main__":

    modes_data = return_modes(app_key=API_KEY)
    modes = tfl_modes(modes_data)

    modes = [mode for mode in modes if mode.lower() in ['tube','overground']]

    try:
        while True:
            main_app(modes)
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
