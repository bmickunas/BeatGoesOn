BeatGoesOn
Created by Sam Hatfield and Bradley Mickunas
==========
1)Create your own local settings file:
    1) Create "settings_local.py" in the main directory of the application.
    2) Paste the following text into your "settings_local.py" and then enter your own EchoNest API key in place of "XXXXXXXXX"
    
        # Settings for this app.
        settings = dict(
            api_key = 'XXXXXXXXX'
        )
    
2)Run The Beat Goes On (Playlist Generator) with the real data:
    1) Enter into the command window:
            python beatgoeson.py
    2) Enter the title of the song you want to be the first song of the playlist.
        If their are other songs with the same title or title with the same terms, a list will print out of songs to choose from.
        Looking through the top_1000_songlist.json is also useful for determining if a song is in the data set.

    3) Enter the number of the songs to be included in the playlist.

    4) Enter 'y' or 'n' to indicate whether or not you want to save the playlist in a json format.
       If yes, then enter in a filename and then look in the main directory of the application for the file. 
       
    5) Enter 'y' or 'n' to indicate whether or not you want to generate another playlist
       with a different first song
   
3)Run the tests:
    1) Enter into the command window:
            python beatgoeson_tests.py
        
4)Run the Gradient Descent Learning Algorithm Program:
    1) Enter into the command window:   
            python gradient_descent.py
        This file learns from "training_set.json". 

5)Run the tests for the Gradient Descent Learning Algorithm:
    1) Enter into the command window:
            python gradient_descent_tests.py