import survey

from data_proc.data_proc import tfl_modes, status_proc
from status_api.status import line_status, return_modes
from params import API_KEY

if __name__ == "__main__":

    modes = tfl_modes(return_modes(app_key=API_KEY))

    mode_idx = survey.routines.select('Please select a TFL service: '
                                   , options = modes)

    chosen_mode = modes[mode_idx]

    line_status = status_proc(line_status(app_key=API_KEY
                                          , modes=chosen_mode))

    print(f"\nThere is {line_status} on the {chosen_mode}")
