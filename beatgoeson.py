'''
beatgoeson.py - Script and supporting classes, functions and data structures
    for BeatGoesOn, our continuous song playlist generator.
Authors: Sam Hatfield and Bradley Mickunas
Date: December 12, 2012
'''

import math
import utils
import ujson
import json

dim_full_set = ['danceability','energy','speechiness', 'liveness', 
                    'tempo', 'loudness',
                'mode','key','time_signature'
                ]

dim_small_set = ['danceability','energy','tempo']

# the max and min values for normalization into a 0.0-1.0 space
norm_ref = {
    'key': {'max': 11.0, 'min': 0.0},
    'loudness': {'max': 0.5, 'min': -52.0},
    'tempo': {'max': 265.0, 'min': 0.0},
    'mode': {'max': 1.0, 'min': 0.0},
    'time_signature': {'max': 7.0, 'min': 0.0}
    }

'''
This nested list structure allows us to remap the keys as reported by Echo Nest
to the Circle of Fifths defined in music theory, giving more accurate key
similarity.
'''
key_remap = [
    #array 0: minor mode
    #0  1   2   3   4   5   6   7   8   9   10  11 (mapping index)
    #C  Cs  D   Eb  E   F   Fs  G   Gs  A   Bb  B  (original order)
    #a  e   b   fs  cs  gs  eb  bb  f   c   g   d  (new mapping order)
    [9, 4,  11, 6,  1,  8,  3,  10, 5,  0,  7,  2],
    #array 1: major mode
    #0  1   2   3   4   5   6   7   8   9   10  11 (mapping index)
    #C  Cs  D   Eb  E   F   Fs  G   Ab  A   Bb  B  (original order)
    #C  G   D   A   E   B   Fs  Cs  Ab  Eb  Bb  F  (new mapping order)
    [0, 7,  2,  9,  4,  11, 6,  1,  8,  3,  10, 5]
    ]

'''
These weights were determined by our machine learning algorithm, which is based
on gradient descent. Relatively larger values increase the importance of a
given feature, while smaller values decrease a feature's importance in
similarity calculation.
'''
weights = {
    'danceability': 1.7025,
    'energy': 1.7199,
    'speechiness': 1.0598,
    'liveness': 1.8126,
    'tempo': 1.5437,
    'loudness': 2.1480,
    'mode': 1.6917,
    'key': 1.4571,
    'time_signature': 1.7686
    }

class BeatGoesOn(object):
    """ 
    A searchommender (search/reccommender) for a continuous & smooth playlist 
    of songs.
    """
    
    def __init__(self):
        self.song_space = [] # vector space of all songs to choose from   

    
    def vectorize(self, songs):
        '''
        Reads in data and creates normalized 'vector' data structures
        for each song.
        Parameters:
            songs - list of songs read in from a cleanly-formatted json file.
        '''
        # songs is the list of nice data structures with the info we need
        for song in songs:
            #remap the key ordering to circle of fifths
            song['key'] = key_remap[song['mode']][song['key']]
            # get the normalized vector of for the song characteristics
            song['vect'] = self.normed_vect(song)
            # store song in song_space
            self.song_space.append(song)
            
    def normed_vect(self, song):
        '''
        Creates vector of normalized data for a song.
        Parameters:
            song - a song data dict.
        '''
        # Create the vector that has the dimensions with scores
        #vect = {dim:song[dim] for dim in dim_full_set}
        vect = {}
        # Make all scores between 0 and 1 by using the max and min values
        #    for that specific field from the EchoNest API
        for dim in dim_full_set:
            vect[dim] = song[dim]
            if dim in norm_ref:
                normed_score = ((float(vect[dim]) - norm_ref[dim]['min'])
                                / (norm_ref[dim]['max'] - norm_ref[dim]['min']))
                vect[dim] = normed_score
            vect[dim] = float(vect[dim]) * weights[dim]
        return vect       
    
    def searchommend(self, seed, playlist):
        '''
        Calculates similarity value between song and all songs in song_space,
        then picks the most similar song for the next entry in playlist.
        Parameters:
            seed - Song we are comparing against (previous entry in playlist)
            playlist - current list of songs, used to make sure we don't pick
                the same song twice
        '''
        most_similar = []

        for song in self.song_space:
            # first, we check if the same song is already in the playlist
            already_found = False
            for item in playlist:
                # if the title of the song under review shows up in
                #another title in the playlist and the artist is the same,
                # throw out the song under review
                if ((item['title'].lower() in song['title'].lower()
                     or song['title'].lower() in item['title'].lower())
                        and item['artist_name'] == song['artist_name']):
                    already_found = True
            if already_found:
                continue

            # Calculate the Euclidian Distance between the seed and all songs
            total = 0
            for dim in dim_full_set:
                diff = seed['vect'][dim] - song['vect'][dim]
                # for key, we use a circular distance measure
                # (i.e. a key of 11 is next to 0)
                # if the diff is more than 6, there is a shorter route on the
                # other side of the circle
                if dim == 'key' and abs(diff) > (6.0/11.0):
                        diff = (12.0/11.0) - abs(diff)
                total += diff**2
            eucl_dist = math.sqrt(total)
            
            # if a minimum hasn't been set yet, use this song
            if (len(most_similar) == 0): 
                most_similar.append(song)
                most_similar.append(eucl_dist)
                #print '\tFirst result:', song['title'], ',', eucl_dist
                #for dim in dim_full_set:
                    #print '\t\t', dim, song[dim]
            else:
                # if the distance is less than the minimum, use this song
                if ((eucl_dist < most_similar[1]) and (playlist.count(song)==0)):
                    most_similar[0] = song
                    most_similar[1] = eucl_dist
                    #print '\tNew max:', song['title'], ',', eucl_dist
                    #for dim in dim_full_set:
                        #print '\t\t', dim, song[dim]
        return most_similar[0]        
        
    def generate_playlist(self, play_count, initial_song):
        ''''
        Generates a playlist by calling searchommend repeatedly for the desired
        number of songs.
        Parameters:
            play_count - the number of songs for the playlist
            initial_song - the song dict selected by the user
        '''
        playlist = []
        playlist.append(initial_song)
        result = self.searchommend(initial_song, playlist)
        playlist.append(result)
        for i in range(play_count-2):
            result = self.searchommend(result, playlist)
            playlist.append(result)
        return playlist        
        
if __name__ == '__main__':
    '''
    When run from the command line, this script loads the data in
    'clean_full_data.json' (a hardcoded filename) and runs the BeatGoesOn user
    program.
    Input:
        clean_full_data.json - a list of cleanly-formatted song dicts
        user input - decisions on input songs, number of songs, and output
    Output:
        text displayed on command line
        'xxxxxx.json' - user-defined output file for playlists
    '''
    beatbox = BeatGoesOn()
    print "Reading Data..."
    data_file = open("clean_full_data.json", 'r')
    data = ujson.load(data_file)
    data_file.close()
    beatbox.vectorize(data)
    print "Initializing Data..."
    while(1):
        print "Enter the title of your first song:"
        title = raw_input('--> ')
        seed = {}
        results = []
        for song in beatbox.song_space:
            if title.lower() in song['title'].lower():
                results.append(song)
        if len(results) == 0:
            print "Error: Song not found in our database. Please try again."
            continue
        elif len(results) > 1:
            print "Found multiple results:"
            i = 1
            for result in results:
                print i,".) ", result['title'], " by ", result['artist_name']
                i +=1
            print "Enter number of the correct song (or -1 if not found):"
            selection = raw_input('--> ')
            if int(selection) < 0 or int(selection) > len(results):
                print "Error: Number invalid. Please try again."
                continue
            seed = results[int(selection) - 1]
        else:
            seed = results[0]
                
        print "Enter how many songs you want on the playlist:"
        song_num = raw_input('--> ')
        groovy_playlist = beatbox.generate_playlist(int(song_num),seed)  
        i = 1
        print "Results:"
        for song in groovy_playlist:
            print i,".) ", song['title'], " by ", song['artist_name']
            for dim in dim_full_set:
                print '\t', dim, song[dim]
            i = i + 1
        print "Save this playlist to json? y/n"
        response = raw_input('--> ')
        if response[0] == 'y':
            print "Please enter 'filename.json':"
            filename = raw_input('--> ')
            output_file = open(filename, 'w')
            json.dump(groovy_playlist, output_file, indent=4)
            output_file.close()
        print "Retry? y/n"
        response = raw_input('--> ')
        if response[0] == 'n':
            break
