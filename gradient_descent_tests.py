import unittest
import gradient_descent

dim_full_set = ['danceability','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']
                        
equal_pair = ({'key': 2, 'title': 'equal_0', 'energy': 0.4, 'liveness': 0.1,
 'tempo': 91.9,
 'speechiness': 0.1, 'artist_name': 'Rihanna', 'vect': {'time_signature': 0.5,
 'energy': 0.4, 'liveness': 0.1, 'tempo': 0.3, 'speechiness': 0.1,
 'danceability': 0.5, 'key': 0.2, 'loudness': 0.8, 'mode': 0.0}, 'mode': 0,
 'time_signature': 4, 'duration': 225.2273, 'loudness': -6.7379999999999995,
 'danceability': 0.547264495122005},
 {'key': 2, 'title': 'equal_1', 'energy': 0.4, 'liveness': 0.1, 'tempo': 91.9,
 'speechiness': 0.1, 'artist_name': 'Rihanna', 'vect': {'time_signature': 0.5,
 'energy': 0.4, 'liveness': 0.1, 'tempo': 0.3, 'speechiness': 0.1,
 'danceability': 0.5, 'key': 0.2, 'loudness': 0.8, 'mode': 0.0}, 'mode': 0,
 'time_signature': 4, 'duration': 225.2273, 'loudness': -6.7379999999999995,
 'danceability': 0.547264495122005})
 
pair_error_of_half = ({'key': 2, 'title': 'halferror_0', 'energy': 0.4, 'liveness': 0.1,
 'tempo': 91.9,
 'speechiness': 0.1, 'artist_name': 'Rihanna', 'vect': {'time_signature': 0.5,
 'energy': 0.4, 'liveness': 0.1, 'tempo': 0.3, 'speechiness': 0.1,
 'danceability': 0.5, 'key': 0.2, 'loudness': 0.8, 'mode': 0.0}, 'mode': 0,
 'time_signature': 4, 'duration': 225.2273, 'loudness': -6.7379999999999995,
 'danceability': 0.547264495122005},
 {'key': 2, 'title': 'halferror_1', 'energy': 0.4, 'liveness': 0.1, 'tempo': 91.9,
 'speechiness': 0.1, 'artist_name': 'Rihanna', 'vect': {'time_signature': 0.5,
 'energy': 0.4, 'liveness': 0.1, 'tempo': 0.3, 'speechiness': 0.1,
 'danceability': 0.1, 'key': 0.3, 'loudness': 0.6, 'mode': 0.0}, 'mode': 0,
 'time_signature': 4, 'duration': 225.2273, 'loudness': -6.7379999999999995,
 'danceability': 0.547264495122005})
 
training_set = [equal_pair,pair_error_of_half]
training_weights = {'time_signature': 1.25, 'energy': 1.2, 'liveness': 1.05,
 'tempo': 1.15, 'speechiness': 1.05, 'danceability': 1.25, 'key': 1.1,
 'loudness': 1.4, 'mode': 1.0}
 
zero_weights = {'time_signature': 0.0, 'energy': 0.0, 'liveness': 0.0,
 'tempo': 0.0, 'speechiness': 0.0, 'danceability': 0.0, 'key': 0.0,
 'loudness': 0.0, 'mode': 0.0}
 
delta_weights_one_iter = {'time_signature': 0.25, 'energy': 0.2,
'liveness': 0.05, 'tempo': 0.15, 'speechiness': 0.05,
'danceability': 0.25, 'key': 0.1, 'loudness': 0.4, 'mode': 0.0}
 
class TestGradientDescent(unittest.TestCase):
    def setUp(self):
        self.learner = gradient_descent.GradientDescent()
    def test_ZeroError(self):
        self.assertAlmostEqual(0.0, self.learner._error(equal_pair[0],equal_pair[1]))
    def test_ZeroGradientVector(self):
        delta_weights = self.learner._calc_gradient(
                    self.learner.learning_rate,0,equal_pair[0])
        for dim in dim_full_set:
            self.assertEqual(zero_weights[dim], delta_weights[dim])
    def test_Error(self):
        self.assertAlmostEqual(0.5, abs(self.learner._error(pair_error_of_half[0],
                                                            pair_error_of_half[1])))
    def test_GradientVector(self):
        delta_weights = self.learner._calc_gradient(
                1.0, 0.5,
                    pair_error_of_half[0])
        print delta_weights
        for dim in dim_full_set:
            #print "dim: ", dim
            self.assertAlmostEqual(delta_weights_one_iter[dim],
                        delta_weights[dim])
    def test_Learn(self):
        self.learner.learn(training_set)
        for dim in dim_full_set:
           # print dim
            self.assertAlmostEqual(training_weights[dim], self.learner.model[dim])
            
if __name__ == '__main__':
    unittest.main()            
            