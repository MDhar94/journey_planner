# Functionality: Data processing functions for the TFL API

def tfl_modes(mode_api_data, reduced_modes=True) -> list:

    """
    Returns a list of all possible 'modes' on the TFL network
    Cleans up the API output

    Params:
        mode_api_data (list): The data from the TFL API
        reduced_modes (bool): Whether to return only the modes of interest

    Returns:
        list: TFL modes as a list
    """

    modes = [mode['modeName'].replace("-"," ").capitalize()
             for mode in mode_api_data]

    if reduced_modes:
        modes = [mode for mode in modes if mode.lower() in ['tube','overground']]

    return modes

def status_proc(status_data, is_tube=False) -> dict:

    """
    Given the data from the TFL line API, returns the status of a 'mode'
    alongside the numeric code for that status

    Params:
        status_data (dict): The data from the TFL API
        is_tube (bool): Whether the mode is the tube

    Returns:
        dict: The status of the specific mode
    """

    service_dict = {'line_id':[], 'line_name':[],'status':[],'status_code':[], 'reason':[]}

    if is_tube:

        for x in status_data:

            line_id = x['id']
            line_name = x['name']
            status = x['lineStatuses'][0]['statusSeverityDescription']
            status_code = x['lineStatuses'][0]['statusSeverity']
            reason = None

            if status_code != 10:
                reason = x['lineStatuses'][0]['reason'].split(':')[1]

            service_dict['line_id'].append(line_id)
            service_dict['line_name'].append(line_name)
            service_dict['status'].append(status)
            service_dict['status_code'].append(status_code)
            service_dict['reason'].append(reason)

    else:

        line_id = status_data[0]['id']
        line_name = status_data[0]['name']
        status = status_data[0]['lineStatuses'][0]['statusSeverityDescription']
        status_code = status_data[0]['lineStatuses'][0]['statusSeverity']
        reason = None

        if status_code != 10:
            reason = status_data[0]['lineStatuses'][0]['reason'].split(':')[1]

        service_dict['line_id'].append(line_id)
        service_dict['line_name'].append(line_name)
        service_dict['status'].append(status)
        service_dict['status_code'].append(status_code)
        service_dict['reason'].append(reason)

    return service_dict
