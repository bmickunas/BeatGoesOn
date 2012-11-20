import unittest
import beatgoeson

song1 = {'title':'Billie Jean','artist':'Michael Jackson',
        'danceability': 0.9, 'energy': 0.9,'key':1, 'tempo':100}

class TestVectorize(unittest.TestCase):
    def test_normalize(self):
        self.v = beatgoeson.BeatGoesOn();
        
        pass

if __name__ == '__main__':
    unittest.main()