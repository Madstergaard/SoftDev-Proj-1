import tix, sift, requests, json


# Takes event list (list of dicts), sorts by date
def sort_by_date(event_list):
    ret = sorted(event_list, key=lambda k: k['date'])
    return ret

# Takes event list, groups by status
# Returns dict of three separate event lists (going/interested/unmarked)
# Still hasn't been tested because we haven't implemented statuses yet
def sort_by_status(event_list):
    inorder = sorted(event_list, key=lambda k: k['status'])
    ret = {}
    for eventdict in inorder:
        status = eventdict['status']
        if status in inorder:
            ret['status'].append(eventdict)
        else:
            ret['status'] = [eventdict]
    for group in ret:
        group = sort_by_date(group)
    return ret
