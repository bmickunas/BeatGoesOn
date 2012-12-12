import unittest
import beatgoeson


expected_keys_small = ['danceability','energy','liveness']
expected_keys_large = ['danceability','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']
expected_norms = {
    'energy': 0.5,
    'tempo': 0.5,
    'speechiness': 0.5,
    'key': 0.5,
    'liveness': 0.5,
    'mode': 1,
    'time_signature': 0.5,
    'loudness': 0.5,
    'danceability': 0.5
    }
    
mock_data = [
    {
        'title': 'Lower',
        'artist_name': 'Downer',
        'energy': 0.3,
        'tempo': 150.0,
        'speechiness': 0.3,
        'key': 3.0,
        'duration': 60.0,
        'liveness': 0.3,
        'mode': 1.0,
        'time_signature': 3.0,
        'loudness': -40.0,
        'danceability': 0.3
    },
    {
        'title': 'Low',
        'artist_name': 'Down',
        'energy': 0.4,
        'tempo': 200,
        'speechiness': 0.4,
        'key': 4,
        'duration': 60,
        'liveness': 0.4,
        'mode': 1,
        'time_signature': 3,
        'loudness': -20,
        'danceability': 0.4
    },
    {
        'title': 'Middle',
        'artist_name': 'Man',
        'energy': 0.5,
        'tempo': 250.0,
        'speechiness': 0.5,
        'key': 5.0,
        'duration': 60.0,
        'liveness': 0.5,
        'mode': 1,
        'time_signature': 3,
        'loudness': 0,
        'danceability': 0.5
    },
    {
        'title': 'Higher',
        'artist_name': 'Upper',
        'energy': 0.7,
        'tempo': 350,
        'speechiness': 0.7,
        'key': 7,
        'duration': 60,
        'liveness': 0.7,
        'mode': 1,
        'time_signature': 3,
        'loudness': 40,
        'danceability': 0.7
    },
    {
        'title': 'Highest',
        'artist_name': 'Top',
        'energy': 1.0,
        'tempo': 500,
        'speechiness': 1.0,
        'key': 10,
        'duration': 60,
        'liveness': 1.0,
        'mode': 1,
        'time_signature': 3,
        'loudness': 100,
        'danceability': 1.0
    }
]



class TestVectorize(unittest.TestCase):
    # perform necessary actions for other tests
    def setUp(self):
        self.beatbox = beatgoeson.BeatGoesOn()
        self.beatbox.vectorize(mock_data)
        
    # vectorize was already run in setUp(), so let's check it               
    def test_vectorize(self):
        # check that the length of song space matches the length of mock_data
        self.assertEqual(len(self.beatbox.song_space), len(mock_data))
        # make sure that the song space has the expected features
        self.assertEqual(set(self.beatbox.song_space[0]['vect'].keys()), 
                        set(expected_keys_large))

    def test_normed_vect(self):
        vector = self.beatbox.normed_vect(mock_data[2])
        # Test the normalization of the song vectors
        for dim in vector:
            self.assertEqual(vector[dim], expected_norms[dim])

    def test_searchommend(self):
        playlist = []
        result = self.beatbox.searchommend(mock_data[2], playlist)
        # if we call search w/ an empty list, the result should be the input
        self.assertEqual(result, mock_data[2])
        # now add the seed to the playlist as we expect
        playlist.append(mock_data[2])
        result2 = self.beatbox.searchommend(mock_data[2], playlist)
        # this time we shouldn't return the input song
        self.assertNotEqual(result2, mock_data[2])
        # the closest song should be "Low" in mock_data
        self.assertEqual(result2, mock_data[1])

    def test_generate_playlist(self):
        playlist = self.beatbox.generate_playlist(5, mock_data[2])
        # make sure the returned playlist has the requested length
        self.assertEqual(len(playlist), 5)
        # Make sure there are no duplicates
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                else:
                    self.assertNotEqual(playlist[i], playlist[j])
        # now check if the playlist has the correct order
        self.assertEqual(playlist[0], mock_data[2])
        self.assertEqual(playlist[1], mock_data[1])
        self.assertEqual(playlist[2], mock_data[0])
        self.assertEqual(playlist[3], mock_data[3])
        self.assertEqual(playlist[4], mock_data[4])
        

if __name__ == '__main__':
    unittest.main()
