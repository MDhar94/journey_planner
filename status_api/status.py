import requests

def line_status(app_key):

    base_url = 'https://api.tfl.gov.uk/BikePoint'
    params_dict = {'app_key':app_key}

    res = requests.get(base_url,params_dict).json()

    return res
