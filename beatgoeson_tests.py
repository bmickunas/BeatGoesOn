import unittest
import beatgoeson

num_of_test_songs = 5
expected_keys = ['FILL ME IN', 'PLEASE']

class TestVectorize(unittest.TestCase):
    def setUp(self):
        self.beatbox = beatgoeson.BeatGoesOn()
        #setup hasn't been written yet, but it should read data and call
        #   vectorize
        self.beatbox.setup(test_data)
        #alternatively, we could also just consolidate setup into vectorize
        #or maybe a wrapper class should read in the data, like in the HWs
        #then we could use a "test_corpus" stored here in the tests file
                
    def test_vectorize(self):
        #vectorize was already run in setUp(), so let's check it
        self.assertEqual(len(self.beatbox.song_space), num_of_test_songs)
        self.assertEqual(self.beatbox.song_space[0].keys(), expected_keys)

    def test_normed_vect(self):
        vector = self.beatbox.normed_vect(sample_song)
        for dim in vector:
            self.assertEqual(vector[dim], expected[dim])

    def test_searchommend(self):
        playlist = []
        result = self.beatbox.searchommend(sample_song, playlist)
        self.assertEqual(result, sample_song)
        playlist.append(sample_song)
        result2 = self.beatbox.searchommend(sample_song, playlist)
        self.assertNotEqual(result, sample_song)
        self.assertEqual(result, close_song)

    def test_generate_playlist(self):
        playlist = self.beatbox.generate_playlist(5, sample_song)
        self.assertEqual(len(playlist), 5)
        for song in playlist:
            for other_song in playlist:
                self.assertNotEqual(song, other_song)

        self.assertEqual(playlist[0], sample_song)
        self.assertEqual(playlist[1], close_song)
        self.assertEqual(playlist[2], close_song2)
        #etc. TODO - finish this as above
        

if __name__ == '__main__':
    unittest.main()
