'''
gradient_descent.py - Gradient descent algorithm for machine learning
    weights for features in BeatGoesOn.
Author: Bradley Mickunas
Date: December 12, 2012
'''
import ujson as json

# Full set of song features that are used as dimensions for song vectors

dim_full_set = ['danceability','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']

class GradientDescent(object):
    def __init__(self):
        self.model = {} # dictionary of dimension weights
        for dim in dim_full_set:
            self.model[dim] = 1.0 # Initialize the weights in the model for each dimension to 1.0
        self.learning_rate = 1.0 # Initialize the learning rate for machine learning to 1.0
        self.N = 1.0 # Number of song pairs that have gone through the learning algorithm. 
    
    def _error(self, input, target_song):
        # Calculate the difference between the summation of the target song and the output from using the model
        actual_output = 0.0 
        target_output = 0.0
        for dim in dim_full_set:
            actual_output = actual_output + input['vect'][dim]*self.model[dim]
        for dim in target_song['vect']:
            target_output = target_output + target_song['vect'][dim]
        return abs(target_output - actual_output) # Take the absolute value of the error between the two song vectors
    
    def _calc_gradient(self, learning_rate, loss, input):
        delta_weight = {} # The gradient vector that holds the calculated change for each dimension in the model
        for dim in dim_full_set:
            delta_weight[dim] = learning_rate*loss*input['vect'][dim] 
        return delta_weight
        
    def learn(self, song_pairs):
        # The song_pairs parameter is a list of "Good" song pairs that would succeed each other in the playlist well
        for pair in song_pairs:         
            loss = self._error(pair[0], pair[1])
            # Compute the adjustment to the weights, delta_w = alpha*(dL/dw),
            del_w = self._calc_gradient(self.learning_rate, loss, pair[0])
            # Update the weights vector, w_2 = w_1 + delta_w
            for key in self.model.iterkeys():
                self.model[key] = self.model[key] + del_w[key]
            # Adjust the learning rate according to the number of song pairs that have passed through the algorithm
            self.learning_rate = self.learning_rate/(self.N**(0.5))
            self.N = self.N + 1.0 # Increment that count for the number of pairs that have trained the model
                
if __name__ == '__main__':
    learner = GradientDescent()
    print "Reading Training Set..."
    data_file = open("training_set.json",'r')
    loaded_training_set = json.load(data_file)
    print "Learning..."
    learner.learn(loaded_training_set)
    print learner.model
