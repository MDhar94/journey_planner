def tfl_modes(mode_api_data):

    modes = [mode['modeName'].replace("-"," ").capitalize()
             for mode in mode_api_data]

    return modes

def status_proc(status_data):

    status = status_data[0]['lineStatuses'][0]['statusSeverityDescription']

    return status
