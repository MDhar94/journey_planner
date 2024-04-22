def tfl_modes(mode_api_data, reduced_modes=True):

    """Returns a list of all possible 'modes' on the TFL network"""

    modes = [mode['modeName'].replace("-"," ").capitalize()
             for mode in mode_api_data]

    if reduced_modes:
        modes = [mode for mode in modes if mode.lower() in ['tube','overground']]

    return modes

def status_proc(status_data):

    """Given the data from the TFL line API, returns the status of a 'mode'
    alongside the numeric code for that status"""

    status = status_data[0]['lineStatuses'][0]['statusSeverityDescription']
    status_code = status_data[0]['lineStatuses'][0]['statusSeverity']

    return status.lower(), status_code

def issue_reason(status_data):

    """Returns the description of why a 'mode' is being impacted
    by an issue"""

    return status_data[0]['lineStatuses'][0]['reason']
