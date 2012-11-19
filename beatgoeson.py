dim_full_set = ['danceability','duration','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']
dim_small_set = ['danceability','energy','key']
                            
class BeatGoesOn(object):
    """ 
    A searchommender (search/reccommender) for continuous playlist 
    of songs 
    """
    
    def __init__(self):
        self.song_space = {} # vector space of all songs to choose from
        
    def vectorize(self, songs):
        # make sure all values are normalized
        for song in songs:
            song['vect'] = self.normed_vect(song)
            # store song in song_space
            self.song_space.append(song);
    def normed_vect(self, song):
        # Create the vector that has the dimensions with scores
        vect = {dim:song[dim] for dim in dim_small_set}
          # calculate the magnitude of the vector
        # What about the values that are already normalized
        for dim in dim_small_set:
            mag = math.sqrt(sum(song[dim]**2))
        return {dim:weight/mag for dim,score in vect.iteritems()}
        pass
    
    def searchommend(self, song):
        # calculate similarity value between song and all songs 
        #   in song_space
        
        # store each sim value inside corresponding song object 
        #   in 'sim'
        pass
    def generate_playlist(self, play_count, initial_song):
        # searchomement play_count songs 
        # return list of songs
        pass 