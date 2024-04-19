import survey

from data_proc.data_proc import issue_reason, tfl_modes, status_proc
from status_api.status import line_status, return_modes
from params import API_KEY

if __name__ == "__main__":

    modes_data = return_modes(app_key=API_KEY)
    modes = tfl_modes(modes_data)

    mode_idx = survey.routines.select('Please select a TFL service: '
                                   , options = modes)

    chosen_mode = modes[mode_idx]

    line_data = line_status(app_key=API_KEY, modes=chosen_mode)
    line_status, line_status_code = status_proc(line_data)

    if line_status_code == 10:

        print(f"\nThere is {line_status} on the {chosen_mode}")

    else:

        reason = issue_reason(line_data).split(':')[1]

        print('Bad luck friend')
        print(f"The {chosen_mode} is experiencing a {line_status.lower()}")
        print(f'The reason is:')
        print(reason.strip())
