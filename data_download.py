'''
data_download.py - Script and functions for downloading Echo Nest API data
    for use in BeatGoesOn.
Author: Sam Hatfield
Date: December 12, 2012
'''

#!/usr/bin/env python
import requests
import ujson as json
import time
import json
import utils
from settings import settings

prev_headers = {}

def rate_limit_wait(headers, thresh = 30, wait_time = 2):
    '''
    A function to make our program wait so that we don't hit the rate limit.
    Parameters:
        header - the dict headers object returned as part of requests.get
        thresh - the threshold at which we start waiting
        wait_time - the amount of time to wait, in seconds
    NOTE: Occasionally, despite this function, we hit the rate limit.
        We feel that this is due to the fact that the RateLimit-Remaining
        is stated to be an estimate by Echo Nest.
    '''
    if int(headers['X-RateLimit-Remaining']) <= 6:
        print 'Hard limit reached, wait for 10 seconds'
        time.sleep(10)
    if int(headers['X-RateLimit-Remaining']) <= thresh:
        print 'Near rate limit, waiting for', wait_time, 'seconds.'
        time.sleep(wait_time)
        
def get_top_artists(hundreds=10):
    '''
    Retrieves up to 1000 of the "hotttest" artists as defined by Echo Nest."
    Parameters:
        hundreds - specify how many results you want in hundreds
    '''
    s_params = {}
    s_params['api_key'] = settings['api_key']
    s_params['bucket'] = ['id:spotify-WW']
    s_params['limit'] = 'true'
    s_params['results'] = '100'

    top_hottt_url = 'http://developer.echonest.com/api/v4/artist/top_hottt'

    my_results = []
    global prev_headers

    # this is a reference so we can easily see what artists we downloaded
    log_file = open("get_top_artists_log.txt", 'w')

    # initialize prev_headers for rate_limit_wait()
    if prev_headers == {}:
        print 'Initializing rate limit...'
        prev_headers = {'X-RateLimit-Remaining': '120'}

    for i in range(0, hundreds):
        #print 'Downloading', i, 'th hundred artists...'
        s_params['start'] = i*100
        rate_limit_wait(prev_headers)
        raw_results = requests.get(top_hottt_url, params=s_params)
        results = raw_results.json
        prev_headers = raw_results.headers

        # check to make sure our search worked correctly
        if results['response']['status']['code'] != 0:
            print 'Search error!'
            print results['response']['status']
            log_file.write('Search error!\n')
            log_file.write("\t" + results['response']['status'] + '\n')
            break
        results_count = len(results['response']['artists'])
        
        for j in range(results_count):
            artist = results['response']['artists'][j]
            json.dump(artist['name'], log_file, indent=4)
            log_file.write('\n')
            my_results.append(artist)
        # break if Echo Nest stops returning results for this query
        if results_count < 100:
            break

    log_file.close()
    return my_results

def get_song_results(s_params, hundreds=10):
    '''
    Retrieves up to 1000 results for a particular song search query.
    Parameters:
        s_params - search parameters for the query. A few of these are set
            internally, but the search-focused parameters are left
            to be specified by the caller.
        hundreds - specify how many hundred results you want from the query
    Returns:
        my_results - a list of songs with our added data
    '''
    
    if 'api_key' not in s_params:
        s_params['api_key'] = settings['api_key']
    s_params['bucket'] = ['audio_summary', 'id:spotify-WW', 'tracks']
    s_params['limit'] = 'true'
    s_params['results'] = '100'

    search_url = 'http://developer.echonest.com/api/v4/song/search'

    my_results = []
    global prev_headers
    
    # initialized for the use of rate_limit_wait()
    if prev_headers == {}:
        print 'Initializing rate limit...'
        prev_headers = {'X-RateLimit-Remaining': '120'}

    for i in range(0, hundreds):
        #print 'Downloading', i, 'th hundred songs...'
        # enclose this in a loop so we can retry our query if needed
        while True:
            s_params['start'] = i*100
            rate_limit_wait(prev_headers)
            raw_results = requests.get(search_url, params=s_params)
            results = raw_results.json
            prev_headers = raw_results.headers

            # check to make sure our search worked correctly
            if results['response']['status']['code'] != 0:
                print 'Search error!'
                print results['response']['status']
                print "Trying again..."
                continue
            results_count = len(results['response']['songs'])
            #print "number of results:", results_count
            for j in range(results_count):
                #print j
                song = results['response']['songs'][j]
                # The code below downloads a detailed analysis of the song.
                # We didn't end up using this data.
                '''
                detail_url = song['audio_summary']['analysis_url']
                #print detail_url
                analysis = requests.get(detail_url)
                #print analysis.status_code
                song['analysis'] = analysis.json
                song['search_rank'] = i*100 + j
                '''
                my_results.append(song)
            break
        # break if Echo Nest stops returning results for this query
        if results_count < 100:
            break

    return my_results

if __name__ == "__main__":
    '''
    When run from the command line, this script downloads the top 100 songs
    from the top 1000 artists (as ranked by Echo Nest).
    Output:
        get_top_artists_log.txt - A list of all artists downloaded.
        full_data_index.json - A list of all songs downloaded, sorted by artist.
        clean_full_data.json - Downloaded song data, reorganized into an
            easy-to-use list of dicts.
    '''
    start_time = time.time()
    print "Starting getting artists..."
    artists = get_top_artists()
    end_time = time.time()
    print 'Got artists after %.3f seconds\n'%(end_time - start_time)

    params = {"sort": "song_hotttnesss-desc"}
    clean_list = {}
    full_data = []

    start_time = time.time()
    print "Starting getting songs..."
    for artist in artists:
        clean_list[artist['name']] = []
        params['artist_id'] = artist['id']
        # query for top 100 songs for this artist
        songs = get_song_results(params, 1)
        for song in songs:
            # add songs to full_data_index
            clean_list[artist['name']].append(song['title'])
        full_data.extend(songs)
        #print 'Got', len(songs), 'songs for', artist['name']
    end_time = time.time()
    print 'Got songs after %.3f seconds\n'%(end_time - start_time)
            
    # a utility function to arrange the data more cleanly
    start_time = time.time()
    print "Starting to reorganize data..."
    nice_data = utils.reorg_songs(full_data)
    end_time = time.time()
    print 'Reorganized data after %.3f seconds\n'%(end_time - start_time)

    start_time = time.time()
    print "Starting data write..."
    data_file = open("clean_full_data.json", 'w')
    json.dump(nice_data, data_file, indent=4)
    data_file.close()
    ref_file = open("full_data_index.json", 'w')
    json.dump(clean_list, ref_file, indent=4)
    ref_file.close()
    end_time = time.time()
    print 'Wrote data after %.3f seconds\n'%(end_time - start_time)
                        
