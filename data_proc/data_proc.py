def tfl_modes(mode_api_data, reduced_modes=True):

    """Returns a list of all possible 'modes' on the TFL network"""

    modes = [mode['modeName'].replace("-"," ").capitalize()
             for mode in mode_api_data]

    if reduced_modes:
        modes = [mode for mode in modes if mode.lower() in ['tube','overground']]

    return modes

def status_proc_dev(status_data, is_tube=False):

    """Given the data from the TFL line API, returns the status of a 'mode'
    alongside the numeric code for that status"""

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

def status_proc(status_data):

    """Given the data from the TFL line API, returns the status of a 'mode'
    alongside the numeric code for that status"""

    status = status_data[0]['lineStatuses'][0]['statusSeverityDescription']
    status_code = status_data[0]['lineStatuses'][0]['statusSeverity']

    return status.lower(), status_code

def status_proc_tube(status_data):

    """Given the data from the TFL line API, returns the status of a 'mode'
    alongside the numeric code for that status - TUBE SPECIFIC"""

    tube_dict = {'line':[],'status':[],'status_code':[]}

    for x in status_data:
        tube_dict['line'].append(x['id'])
        tube_dict['status'].append(x['lineStatuses'][0]['statusSeverityDescription'])
        tube_dict['status_code'].append(x['lineStatuses'][0]['statusSeverity'])

    return tube_dict

def issue_reason(status_data):

    """Returns the description of why a 'mode' is being impacted
    by an issue"""

    return status_data[0]['lineStatuses'][0]['reason']

def issue_reason_tube(status_data):

    """Returns the description of why a 'mode' is being impacted
    by an issue"""

    return status_data['lineStatuses'][0]['reason']
