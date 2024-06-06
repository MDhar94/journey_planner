import os
import pandas as pd

from backend.data.data_proc.data_proc import tfl_modes, status_proc
from backend.data.status_api.status import line_status, return_modes
from params import API_KEY, RAW_DATA_PATH

def get_data() -> pd.DataFrame:

    """
    Creates a dataframe of TFL status data (when not good) to be saved

    Output:
        pd.DataFrame: The status data for the tube and overground services

    """

    modes = [mode.lower() for mode in tfl_modes(return_modes(app_key=API_KEY)) if mode.lower() in ['tube', 'overground']]
    mode_dicts = []

    for mode in modes:

        line_data = line_status(app_key=API_KEY, modes=mode)
        service_dict = status_proc(line_data, is_tube=(mode == 'tube'))
        mode_dicts.append(service_dict)

    # concatenate the dictionaries

    df1 = pd.DataFrame(mode_dicts[0])
    df2 = pd.DataFrame(mode_dicts[1])

    mode_df = pd.concat([df1, df2]).reset_index(drop=True)
    mode_df = mode_df[mode_df['status_code'] != 10]
    mode_df['date'] = pd.to_datetime('today').strftime("%m/%d/%Y, %H:%M")

    return mode_df

if __name__ == "__main__":

    try:
        df = get_data()

        save_path = os.path.join(RAW_DATA_PATH, 'status_data.csv')

        if 'status_data.csv' not in os.listdir('raw_data/'):
            df.to_csv(save_path, index=False)

        elif 'status_data.csv' in os.listdir('raw_data/'):
            df.to_csv(save_path, mode='a', header=False, index=False)

    except Exception as e:

        print(f"Error: {e}")
        print("Exiting...")
        exit(1)
