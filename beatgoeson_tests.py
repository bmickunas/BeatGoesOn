'''
beatgoeson_tests.py - Basic unittests for beatgoeson.py.
Author: Sam Hatfield
Date: December 12, 2012
'''

import unittest
import beatgoeson


expected_keys_small = ['danceability','energy','liveness']
expected_keys_large = ['danceability','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']

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

expected_norms = {
    'energy': 0.5*weights['energy'],
    'tempo': (250.0/265.0)*weights['tempo'],
    'speechiness': 0.5*weights['speechiness'],
    # NOTE: when we run normed_vect directly, keys aren't remapped
    'key': (11.0/11.0)*weights['key'],
    'liveness': 0.5*weights['liveness'],
    'mode': 1.0*weights['mode'],
    'time_signature': (3.0/7.0)*weights['time_signature'],
    'loudness': ((0.0+52.0)/52.5)*weights['loudness'],
    'danceability': 0.5*weights['danceability']
    }
    
mock_data = [
    {
        'title': 'Lower',
        'artist_name': 'Downer',
        'energy': 0.3,
        'tempo': 150.0,
        'speechiness': 0.3,
        'key': 9,   #3 in new mapping
        'liveness': 0.3,
        'mode': 1,
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
        'key': 4,   #4 in new mapping
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
        'key': 11,  #5 in new mapping
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
        'key': 1,   #7 in new mapping
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
        'key': 10,  #10 in new mapping
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
            print dim, ':', vector[dim]
            self.assertAlmostEqual(vector[dim], expected_norms[dim])

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
