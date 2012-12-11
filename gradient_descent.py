dim_full_set = ['danceability','energy','key','loudness',
                    'tempo', 'speechiness', 'liveness', 'mode',
                        'time_signature']

training_pairs =({'key': 2, 'title': 'Diamonds', 'energy': 0.4, 'liveness': 0.1,
 'tempo': 91.9,
 'speechiness': 0.1, 'artist_name': 'Rihanna', 'vect': {'time_signature': 0.5,
 'energy': 0.4, 'liveness': 0.1, 'tempo': 0.3, 'speechiness': 0.1,
 'danceability': 0.5, 'key': 0.2, 'loudness': 0.8, 'mode': 0.0}, 'mode': 0,
 'time_signature': 4, 'duration': 225.2273, 'loudness': -6.7379999999999995,
 'danceability': 0.547264495122005},
 {'key': 2, 'title': 'Diamonds', 'energy': 0.4, 'liveness': 0.1, 'tempo': 91.9,
 'speechiness': 0.1, 'artist_name': 'Rihanna', 'vect': {'time_signature': 0.5,
 'energy': 0.4, 'liveness': 0.1, 'tempo': 0.3, 'speechiness': 0.1,
 'danceability': 0.5, 'key': 0.2, 'loudness': 0.8, 'mode': 0.0}, 'mode': 0,
 'time_signature': 4, 'duration': 225.2273, 'loudness': -6.7379999999999995,
 'danceability': 0.547264495122005})


class GradientDescent(object):
    def __init__(self):
        #self.training_set = [] # Successful song pairs to learn from
        self.model = {} # dict of parameter weights
        for dim in dim_full_set:
            self.model[dim] = 1.0
        self.learning_rate = 1.0
        self.N = 1.0 # number of song_pairs seen; used form the learning_rate
    
    def _error(self, input, target_song):
        actual_output = 0.0
        target_output = 0.0
        for dim in dim_full_set:
            actual_output = actual_output + input['vect'][dim]*self.model[dim]
        for dim in target_song['vect']:
            target_output = target_output + target_song['vect'][dim]
        return abs(target_output - actual_output)
    
    def _calc_gradient(self, learning_rate, loss, input):
        delta_weight = {}
        for dim in dim_full_set:
            #print learning_rate," * ", loss, " * ", input['vect'][dim]
            delta_weight[dim] = learning_rate*loss*input['vect'][dim]
            #print dim,"_w: ", delta_weight[dim]
        #print "Delta_w: ",delta_weight
        return delta_weight
        
    def learn(self, song_pairs):
        # <x, y> - training pair where x and y are successful song pairs
        for pair in song_pairs:         
            # print "Learning from (",pair[0]['title'],", ",pair[1]['title'],")" 
            loss = self._error(pair[0], pair[1])
            # print "Loss: ", loss
            # Compute the adjustment to the weights, delta_w = alpha*(dL/dw),
            del_w = self._calc_gradient(self.learning_rate, loss, pair[0])
            # Update the weights vector, w_2 = w_1 + delta_w
            for key in self.model.iterkeys():
                self.model[key] = self.model[key] + del_w[key]
            self.learning_rate = self.learning_rate/(self.N**(0.5))
            self.N = self.N + 1.0
            # print self.model
                
if __name__ == '__main__':
    learner = GradientDescent()
    print "Reading Training Set..."
    # data_file = open("",'r')
    # training_set = json.load(data_file)
    print "Learning..."
    learner.learn(training_set)
    print learner.model