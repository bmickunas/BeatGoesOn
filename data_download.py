#!/usr/bin/env python
import requests
import ujson as json

def get_song_results(s_params, hundreds=10):
    if 'api_key' not in s_params:
        s_params['api_key'] = 'VSCPXIV4KTWEQ7NFF'
    s_params['buckets'] = ['audio_summary', 'id:spotify-WW', 'tracks']
    s_params['limit'] = 'true'
    s_params['results'] = '100'

    search_url = 'http://developer.echonest.com/api/v4/song/search'

    my_results = []

    for i in range(0, hundreds):
        s_params['start'] = i*100
        raw_results = requests.get(search_url, params=s_params)
        results = raw_results.json
        if results['response']['status']['code'] <> 0:
            print 'Search error!'
        results_count = len(results['response']['songs'])
        for j in range(results_count):
            song = results['response']['songs'][j]
            analysis = results.get(song['audio_summary']['analysis_url'])
            song['audio_summary']['analysis'] = analysis.json
            song['search_rank'] = i*100 + j
            

    
                         
