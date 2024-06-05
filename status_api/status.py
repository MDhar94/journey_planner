import requests
import sys

from params import API_KEY

def return_modes(app_key):

    """Returns the modes (different TFL branches) that are available
    on the API"""

    base_url = f'https://api.tfl.gov.uk/Line/Meta/Modes'
    params_dict = {'app_key':app_key}

    res = requests.get(base_url,params_dict)

    return res.json()

def line_status(app_key, modes):

    """Returns the status data for a given 'mode' of the TFL network"""

    base_url = f'https://api.tfl.gov.uk/Line/Mode/{modes}/Status'
    params_dict = {'app_key':app_key}

    res = requests.get(base_url,params_dict)

    return res.json()

if __name__ == "__main__":

    """Just checking out the format of the data the API returns"""

    res_modes = return_modes(API_KEY)
    modes = [mode['modeName'] for mode in res_modes]

    print(modes)

    mode = sys.argv[1]

    if mode in modes:
        print("Valid mode provided!")
        res = line_status(API_KEY,mode)

        breakpoint()

        status = res[0]['lineStatuses'][0]['statusSeverityDescription']
        status_num = res[0]['lineStatuses'][0]['statusSeverity']

        # print(status)
        # print(status_num)
        # print(res[0]['lineStatuses'][0].keys())
        # breakpoint()
        # print(f"The overground is currently operating with {status}")

    else:
        print("Please provide a valid mode")
