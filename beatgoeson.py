
class BeatGoesOn(object):
    """ 
    A searchommender (search/reccommender) for continuous playlist 
    of songs 
    """
    
    def __init__(self):
        self.song_space = {} # vector space of all songs to choose from
        dimensions = ['danceability','duration','energy','key','loudness',
                        'tempo', 'speechiness', 'liveness', 'mode',
                            'time_signature']
    def vectorize(self, songs):
        # make sure all values are normalized
        for song in songs:
            song['vect'] = self.normed_vect(song)
            # store song in song_space
            self.song_space.append(song);
    def normed_vect(self, song):
        
    
    def searchommend(self, song):
        # calculate similarity value between song and all songs in song_space
        # store each sim value inside corresponding song object in 'sim'
    
    def generate_playlist(self, play_count, initial_song):
        # searchomement play_count songs 
        # return list of songs