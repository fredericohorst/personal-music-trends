import requests
import datetime
import json

from requests.sessions import requote_uri
# http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=rj&api_key=YOUR_API_KEY&format=json




# get recent tracks method:

#TODO:
def lastfm_auth():
    with open('credentials.json', 'r') as credentials:
        c = json.load(credentials)
        api_key = c['API-key']
    auth_link = 'http://www.last.fm/api/auth/?api_key=' + api_key
    return auth_link


def variables(extended, initial_date, end_date):
    """
    Sets variables for requesting LastFM API. 
    Returns a the API link for grabing the data in json format.
    """
    lastfm_api_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'
    # user = 'lastfm-user-name'
    with open('credentials.json', 'r') as credentials:
        c = json.load(credentials)
        api_key = c['API-key']
        user = c['user-name']
    param_extended = str(extended)
    param_from = str(initial_date) # unix timestamp format
    param_to = str(end_date) # unix timestamp format
    request_link = lastfm_api_url + '&user=' + user + '&api_key=' + api_key \
        + '&format=json' + '&extended=' + param_extended + '&from=' + param_from + '&to=' + param_to
    # request_link = lastfm_api_url + '&user=' + user \
    #     + 'format=json' + '&extended=' + param_extended + '&from=' + param_from + '&to=' + param_to
    return request_link


def lastfm_recent_tracks(request_url):
    """
    Requests the data from LastFM API.
    # docs: https://www.last.fm/api/show/user.getRecentTracks
    """
    partial_data = requests.get(request_url)
    partial_data_json = partial_data.json()
    total_pages = int(partial_data_json.get('recenttracks').get('@attr').get('totalPages'))
    partial_data = None
    partial_data_json = None
    lastfm_data_full = []
    for page in range(total_pages):
        request_url = request_url + '&page='+str(page)
        data = requests.get(request_url)
        lastfm_data = data.json()
        lastfm_data_full.append(lastfm_data)
    return lastfm_data_full

def lastfm_last12mos_tracks():
    """
    Requests the data from LastFM API.
    """
    # request_url = variables(extended=)
    from datetime import datetime
    import time
    from dateutil.relativedelta import relativedelta
    today = datetime.today()
    begin = today + relativedelta(months=12)
    begin = time.mktime(begin.timetuple())
    today = time.mktime(today.timetuple())
    request_url = variables(extended='True',initial_date=begin, end_date=today)
    data = requests.get(request_url)
    lastfm_data = data.json()
    return lastfm_data

def saving_lastfm_data(data, file_path):
    import pandas
    from datetime import date, datetime
    lastfm_list = []
    recent_tracks = [i.get('recenttracks', 'track') for i in data]
    for item in recent_tracks:
        if isinstance(item, dict): 
            for track in item.get('track'):
                lastfm_dict = {}
                if isinstance(track.get('artist'), dict): lastfm_dict['artist_name'] = track.get('artist').get('name')
                if isinstance(track.get('date'), dict): lastfm_dict['date_uts'] = track.get('date').get('uts')
                if isinstance(track.get('date'), dict): lastfm_dict['date'] = datetime.fromtimestamp(int(track.get('date').get('uts')))
                lastfm_dict['track_name'] = track.get('name')
                lastfm_dict['loved_track'] = track.get('loved')
                lastfm_list.append(lastfm_dict)
    lastfm_df = pandas.DataFrame(lastfm_list)
    lastfm_df.to_csv(file_path)
    return lastfm_df



# historical data`

# https://blockgeni.com/guide-to-get-music-data-with-the-last-fm-api-using-python/



# http://millionsongdataset.com/lastfm/
