import requests
import datetime
import json

from requests.sessions import requote_uri
# http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=rj&api_key=YOUR_API_KEY&format=json

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
    docs: https://www.last.fm/api/show/user.getRecentTracks
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
    """
    Cleans the json data from LastFM API.
    Saves file into file_path.
    Returns a dataframe to be used.
    """
    import pandas
    from datetime import date, datetime
    lastfm_list = []
    recent_tracks = [i.get('recenttracks', 'track') for i in data]
    for item in recent_tracks:
        if isinstance(item, dict): 
            for track in item.get('track'):
                lastfm_dict = {}
                if isinstance(track.get('artist'), dict): lastfm_dict['artist_name'] = track.get('artist').get('name')
                if isinstance(track.get('album'), dict): lastfm_dict['album_name'] = track.get('album').get('#text')
                if isinstance(track.get('date'), dict): lastfm_dict['date_uts'] = track.get('date').get('uts')
                if isinstance(track.get('date'), dict): lastfm_dict['date'] = datetime.fromtimestamp(int(track.get('date').get('uts')))
                lastfm_dict['track_name'] = track.get('name')
                lastfm_dict['loved_track'] = track.get('loved')
                lastfm_list.append(lastfm_dict)
    lastfm_df = pandas.DataFrame(lastfm_list)
    lastfm_df.to_csv(file_path)
    return lastfm_df

def import_historic_data(file_path, initial_year, end_year):
    """
    Imports all data iterating by every year from the 
    initial_year to the end_year.
    Saves files into file_path + year in CSV format.
    """
    # import lastfm
    from datetime import date, datetime
    import time
    for year in range(initial_year, end_year+1):
        # compose variables:
        begin = date(year,1,1)
        begin = int(time.mktime(begin.timetuple()))
        end = date(year,12,31)
        end = int(time.mktime(end.timetuple()))
        request_link = variables(extended='1', initial_date=begin, end_date=end)
        # requesting data:
        data = lastfm_recent_tracks(request_url = request_link)
        file = file_path + str(year) + '.csv'
        lastfm_df = saving_lastfm_data(data=data, file_path=file)
        print('saved', file)
    return "files saved correctly at " + file_path

