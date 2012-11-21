#!/usr/bin/env python
import requests
import ujson as json
import time
import json
import utils
from settings import settings 

def rate_limit_wait(headers, thresh = 30, wait_time = 2):
    '''
    A function to make our program wait so that we don't hit the rate limit.
    Parameters:
        header - the dict headers object returned as part of requests.get
        thresh - the threshold at which we start waiting
        wait_time - the amount of time to wait, in seconds
    '''
    if int(headers['X-RateLimit-Remaining']) <= thresh:
        print 'Near rate limit, waiting for', wait_time, 'seconds.'
        time.sleep(wait_time)
    

def get_song_results(s_params, hundreds=10):
    '''
    Retrieves up to 1000 results for a particular query.
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
    # initialized for the use of rate_limit_wait()
    prev_headers = {'X-RateLimit-Remaining': '120'}

    for i in range(0, hundreds):
        print 'Downloading', i, 'th hundred songs...'
        s_params['start'] = i*100
        rate_limit_wait(prev_headers)
        raw_results = requests.get(search_url, params=s_params)
        results = raw_results.json
        prev_headers = raw_results.headers
        # check to make sure our search worked correctly
        if results['response']['status']['code'] != 0:
            print 'Search error!'
            print results['response']['status']
            break
        results_count = len(results['response']['songs'])
        #print "number of results:", results_count
        for j in range(results_count):
            #print j
            song = results['response']['songs'][j]
            # Here we skip some detailed data downloading, since we don't
            #   need it yet. This speeds up download speeds significantly.
            '''
            detail_url = song['audio_summary']['analysis_url']
            print detail_url
            analysis = requests.get(detail_url)
            print analysis.status_code
            song['analysis'] = analysis.json
            song['search_rank'] = i*100 + j
            '''
            my_results.append(song)
        # this conditional statement allows us to break if we get less results
        #   than we expected
        if results_count < 100:
            break

    return my_results


if __name__ == "__main__":
    # Right now, our main function is hard-coded to get the top 1000 songs
    params = {"sort": "song_hotttnesss-desc"}
    
    start_time = time.time()
    print "Starting getting results..."
    results = get_song_results(params, 10)
    end_time = time.time()
    print 'Got results after %.3f seconds'%(end_time - start_time)

    # a utility function to arrange the data more cleanly
    start_time = time.time()
    print "Starting to reorganize data..."
    nice_data = utils.reorg_songs(results)
    end_time = time.time()
    print 'Reorganized data after %.3f seconds'%(end_time - start_time)
    
    start_time = time.time()
    print "Starting data write..."
    data_file = open("top_1000_clean_songs.json", 'w')
    json.dump(nice_data, data_file, indent=4)
    # print pretty json objects with the indent=4 parameter
    end_time = time.time()
    print 'Wrote data after %.3f seconds'%(end_time - start_time)
                        
