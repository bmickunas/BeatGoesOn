'''
utils.py - Utility functions for BeatGoesOn.
Authors: Sam Hatfield and Bradley Mickunas
Date: December 12, 2012
'''

import ujson as json
import json
import fileinput

song_ignore = ['search_rank','tracks','audio_md5']
analysis_ignore = ['bars','segments','track','beats','meta',
    'sections','tatums','audio_md5']
audio_summary_ignore = ['audio_md5']

def read_songs():
    for line in fileinput.input():
        yield json.loads(line)
            
seen  = set()

def reorg_songs(songs):
    clean_songs = []
    for song in songs:
        clean_song = {}
        clean_song['title'] = song['title']
        clean_song['artist_name'] = song['artist_name']
        clean_song['energy'] = song['audio_summary']['energy']
        clean_song['tempo'] = song['audio_summary']['tempo']
        clean_song['speechiness'] = song['audio_summary']['speechiness']
        clean_song['key'] = song['audio_summary']['key']
        clean_song['duration'] = song['audio_summary']['duration']
        clean_song['liveness'] = song['audio_summary']['liveness']
        clean_song['mode'] = song['audio_summary']['mode']
        clean_song['time_signature'] = song['audio_summary']['time_signature']
        clean_song['loudness'] = song['audio_summary']['loudness']
        clean_song['danceability'] = song['audio_summary']['danceability']
        clean_songs.append(clean_song)

    return clean_songs
    
    
