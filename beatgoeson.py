import math
import utils
import ujson as json

dim_full_set = ['danceability','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']
dim_small_set = ['danceability','energy','liveness']

norm_ref = {
    'key': {'max': 11.0, 'min': -1.0},
    'loudness': {'max': 100.0, 'min': -100.0},
    'tempo': {'max': 500.0, 'min': 0.0},
    'mode': {'max': 1.0, 'min': -1.0},
    'time_signature': {'max': 7.0, 'min': -1.0}
    }
  
class BeatGoesOn(object):
    """ 
    A searchommender (search/reccommender) for continuous playlist 
    of songs 
    """
    
    def __init__(self):
        self.song_space = [] # vector space of all songs to choose from   
        
    def vectorize(self, songs):
        # songs is the list of nice data structures with the info we need
        for song in songs:
            # get the normalized vector of for the song characteristics
            song['vect'] = self.normed_vect(song)
            # store song in song_space
            self.song_space.append(song)
            
    def normed_vect(self, song):
        # Create the vector that has the dimensions with scores
        vect = {dim:song[dim] for dim in dim_full_set} # or full_set
        # Make all scores between 0 and 1 by using the max and min values
        #    for that specific field from the EchoNest API
        for dim in dim_full_set:
            if dim in norm_ref:
                normed_score = ((float(vect[dim]) - norm_ref[dim]['min'])
                                / (norm_ref[dim]['max'] - norm_ref[dim]['min']))
                vect[dim] = normed_score
        return vect       
    
    def searchommend(self, seed, playlist):
        # calculate similarity value between song and all songs 
        #   in song_space
        most_similar = []
        # Calculate the Euclidian Distance between the seed and all songs
        for song in self.song_space:            
            eucl_dist = math.sqrt(sum(
                    ((seed['vect'][dim]-song['vect'][dim])**2 for dim in dim_full_set)
                    ))              
            # if the song has a lesser euclidian distance 
            #   and it is not already in the playlist
            if (len(most_similar) == 0): 
                if (playlist.count(song)==0):
                    most_similar.append(song)
                    most_similar.append(eucl_dist)
            else:
                if ((eucl_dist < most_similar[1]) and (playlist.count(song)==0)):
                        most_similar[0] = song
                        most_similar[1] = eucl_dist 
        return most_similar[0]        
        
    def generate_playlist(self, play_count, initial_song):
        # searchommend play_count number of songs
        playlist = []
        playlist.append(initial_song)
        result = self.searchommend(initial_song, playlist)
        playlist.append(result)
        for i in range(play_count-2):
            result = self.searchommend(result, playlist)
            playlist.append(result)
        return playlist        
        
if __name__ == '__main__':
    beatbox = BeatGoesOn()
    print "Reading Data..."
    #data = utils.read_songs() # this function is not working for some reason
    data_file = open("top_1000_clean_songs.json", 'r')
    data = json.load(data_file)
    beatbox.vectorize(data)
    print "Initializing Data..."
    while(1):
        print "Enter the title of your first song"
        title = raw_input('--> ')
        seed = {}
        for song in beatbox.song_space:
            if song['title'].lower() == title.lower():
                seed = song
                break
        if len(seed.keys()) == 0:
            print "Error: Song not found"
            continue    
        else:
            print "Enter how many songs you want on the playlist"
            song_num = raw_input('--> ')
            groovy_playlist = beatbox.generate_playlist(int(song_num),seed)  
            i = 1;
            print "Results:"
            for song in groovy_playlist:
                print i,".) ", song['title'], " by ", song['artist_name']
                i = i + 1 
            print "Retry? y/n"
            response = raw_input('--> ')
            if response[0] == 'n':
                break
