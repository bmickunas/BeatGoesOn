#!/usr/bin/env python
import requests
import ujson as json
import time
import json

def get_song_results(s_params, hundreds=10):
    if 'api_key' not in s_params:
        s_params['api_key'] = 'ZSDNTL7YAQRK6028S'
    s_params['bucket'] = ['audio_summary', 'id:spotify-WW', 'tracks']
    s_params['limit'] = 'true'
    s_params['results'] = '10'

    search_url = 'http://developer.echonest.com/api/v4/song/search'

    my_results = []

    for i in range(0, hundreds):
        s_params['start'] = i*100
        raw_results = requests.get(search_url, params=s_params)
        results = raw_results.json
        if results['response']['status']['code'] != 0:
            print 'Search error!'
            print results['response']['status']
        results_count = len(results['response']['songs'])
        #print "number of results:", results_count
        for j in range(results_count):
           # print j
            song = results['response']['songs'][j]
            detail_url = song['audio_summary']['analysis_url']
           # print detail_url
            analysis = requests.get(detail_url)
           # print analysis.status_code
            song['analysis'] = analysis.json
            song['search_rank'] = i*100 + j
            my_results.append(song)
        if results_count < 100:
            break

    return my_results

if __name__ == "__main__":
    params = {"sort": "song_hotttnesss-desc"}
    
    start_time = time.time()
    print "Starting getting results..."
    results = get_song_results(params, 1)
    end_time = time.time()
    print 'Got results after %.3f seconds'%(end_time - start_time)

    start_time = time.time()
    print "Starting data write..."
    analysis_keys = ["tempo", "key", "loudness"]
    filename = "top_100_songs_toexcel.txt" 
    data_file = open(filename,'w')
    for result in results:
        #print format: title    tempo   key    loudness
        data_file.write(result['title']+"\t"+str(result['analysis']['track']['tempo'])+"\t"+
            str(result['analysis']['track']['key'])+"\t"+str(result['analysis']['track']['loudness'])+"\n")
    end_time = time.time()
    print 'Wrote data after %.3f seconds'%(end_time - start_time)