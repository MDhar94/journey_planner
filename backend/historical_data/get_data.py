from google.oauth2 import service_account
import ipdb
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

    print("modes returned")

    for mode in modes:
        line_data = line_status(app_key=API_KEY, modes=mode)
        service_dict = status_proc(line_data, is_tube=(mode == 'tube'))
        mode_dicts.append(service_dict)

    print("Dicts made")

    # concatenate the dictionaries
    df1 = pd.DataFrame(mode_dicts[0])
    df2 = pd.DataFrame(mode_dicts[1])
    mode_df = pd.concat([df1, df2]).reset_index(drop=True)

    print("Dataframe made")

    # mode_df = mode_df[mode_df['status_code'] != 10]
    mode_df['date'] = pd.to_datetime('today').strftime("%m/%d/%Y, %H:%M")

    print("Date added")

    return mode_df

def upload_to_bigquery(df: pd.DataFrame):
    """
    Uploads dataframe to Google BigQuery
    """
    # Construct the BigQuery credentials and client

    print(GOOGLE_APPLICATION_CREDENTIALS)

    print(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

    print("Credentials made")

    # BigQuery Dataset and Table names from environment variables
    full_table_id = f"{DATASET_NAME}.{TABLE_NAME}"

    print(f"Table ID made: {full_table_id}")

    # Uploading to BigQuery
    pandas_gbq.to_gbq(df, full_table_id, project_id=PROJECT_ID, if_exists='append', credentials=credentials)

    print("Data uploaded")

if __name__ == "__main__":

    # try to upload to bigquery, if error print error and set trace to debug

    try:
        print("getting data...")
        df = get_data()
        print("uploading to bigquery...")
        upload_to_bigquery(df)
        print("done!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        ipdb.set_trace()
