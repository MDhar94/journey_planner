import emoji # type: ignore
import survey # type: ignore
import sys

from data_proc.data_proc import issue_reason, tfl_modes, status_proc
from status_api.status import line_status, return_modes
from params import API_KEY

def main_app(modes):

    """The main flow of this app"""

    mode_idx = survey.routines.select('Please select a TFL service: '
                                   , options = modes)

    chosen_mode = modes[mode_idx]

    line_data = line_status(app_key=API_KEY, modes=chosen_mode)
    status, status_code = status_proc(line_data)

    if status_code == 10:
        print(f"\nThere is {status} on the {chosen_mode}\n")

    else:
        reason = issue_reason(line_data).split(':')[1]
        print('Bad luck, friend!')
        print(emoji.emojize(f"The {chosen_mode} is experiencing a :sparkles: {status} :sparkles:"))
        print(f'The reason is:')
        print(reason.strip())

    continue_idx = survey.routines.select('Would you like to check another service?'
                                          , options = ['Yes','No'])

    if continue_idx == 0:
        return True
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
