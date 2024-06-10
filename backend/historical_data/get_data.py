from google.oauth2 import service_account
import os
import pandas as pd
import pandas_gbq

from backend.data.data_proc import tfl_modes, status_proc
from backend.data.status import line_status, return_modes
from backend.logic.params import *

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

def upload_to_bigquery(df: pd.DataFrame):
    """
    Uploads dataframe to Google BigQuery
    """
    # Construct the BigQuery credentials and client
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

    # BigQuery Dataset and Table names from environment variables
    full_table_id = f"{DATASET_NAME}.{TABLE_NAME}"

    # Uploading to BigQuery
    pandas_gbq.to_gbq(df, full_table_id, project_id=PROJECT_ID, if_exists='append', credentials=credentials)

if __name__ == "__main__":
    try:
        df = get_data()
        save_path = os.path.join(RAW_DATA_PATH, 'status_data.csv')

        if 'status_data.csv' not in os.listdir('raw_data/'):
            df.to_csv(save_path, index=False)

        elif 'status_data.csv' in os.listdir('raw_data/'):
            df.to_csv(save_path, mode='a', header=False, index=False)

        upload_to_bigquery(df)

    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
        exit(1)
