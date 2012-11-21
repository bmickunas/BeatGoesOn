import math
dim_full_set = ['danceability','duration','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']
dim_small_set = ['danceability','energy','liveness']

norm_ref = {
    'key': {'max': 11, 'min': -1},
    'loudness': {'max': 100.0, 'min': -100.0},
    'tempo': {'max': 500.0, 'min': 0.0},
    'mode': {'max': 1, 'min': -1},
    'time_signature': {'max': 7, 'min': -1}
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
        vect = {dim:song[dim] for dim in dim_small_set} # or full_set
        # calculate the magnitude of the vector
        # What about the values that are already normalized?
        for dim in dim_small_set:                       #or full_set
            if dim in norm_ref:
                normed_score = ((vect[dim] - norm_ref[dim]['min'])
                                / (norm_ref[dim]['max'] - norm_ref[dim]['min']))
                vect[dim] = normed_score
        return vect       
    
    def searchommend(self, seed, playlist):
        # calculate similarity value between song and all songs 
        #   in song_space
        most_sim_song = ['',0.0]
        print 'Searching for', seed['title'], '...'
        mag_seed = math.sqrt(sum(seed['vect'][dim]**2 for dim in dim_small_set))
        print seed['title'], 'mag is:', mag_seed
        for song in self.song_space:
            print '\tComparing to:', song['title'], '...'
            mag_song = math.sqrt(sum(song['vect'][dim]**2
                                    for dim in dim_small_set))
            print '\t', song['title'], 'mag is:', mag_song
            dot_product = sum(
                    (seed['vect'][dim]*song['vect'][dim] for dim in dim_small_set)
                    )
            print '\t', song['title'], 'dot_prod is:', dot_product
            song['sim'] = dot_product/(mag_seed*mag_song)
            print '\tSim of', song['title'], ':', song['sim']
            # if the song is more similar and it is not already in the playlist
            print '\tCount of song in playlist:', playlist.count(song)
            if ((song['sim'] > most_sim_song[1]) and (playlist.count(song)==0)):                
                most_sim_song[0] = song
                most_sim_song[1] = song['sim']
        print 'Returning', most_sim_song[0]['title'], 'for seed', seed['title']
        return most_sim_song[0]        
        
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
