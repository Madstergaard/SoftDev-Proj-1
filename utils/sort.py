import tix, sift, requests, json


# Takes event list (list of dicts), sorts by date
def sort_by_date(event_list):
    ret = sorted(event_list, key=lambda k: k['date'])
    return ret

