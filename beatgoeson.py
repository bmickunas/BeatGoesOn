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
        # songs is the list of nice data structures with the info we need
        for song in songs:
            # get the normalized vector of for the song characteristics
            song['vect'] = self.normed_vect(song)
            # store song in song_space
            self.song_space.append(song);
    def normed_vect(self, song):
        # Create the vector that has the dimensions with scores
        vect = {dim:song[dim] for dim in dim_small_set}
          # calculate the magnitude of the vector
        # What about the values that are already normalized?
        for dim in dim_small_set:
            mag = math.sqrt(sum(song[dim]**2))
        return {dim:weight/mag for dim,score in vect.iteritems()}        
    
    def searchommend(self, seed, playlist):
        # calculate similarity value between song and all songs 
        #   in song_space
        most_sim_song = ['0',0.0]
        for song in self.song_space:
            song['sim'] = sum(
                    seed['vect'][dim]*song['vect'][dim]
                    for dim in dim_small_set
                    )
            # if the song is more similar and it is not already in the playlist
            if ((song['sim'] > most_sim_song[1])&&(!song.index(song))):                
                most_sim_song[0] = song['spotify_id']
                most_sim_song[1] = song['sim']
        return most_sim_song[0]        
        
    def generate_playlist(self, play_count, initial_song):
        # searchommend play_count number of songs
        result_spot_id = searchommend(initial_song)
        playlist.append(initial_song)
        playlist.append(result_spot_id)
        for i in range(play_count-2):
            result_spot_id = searchommend(result_spot_id)
            playlist.append(result_spot_id)
        return playlist        