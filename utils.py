import ujson
import fileinput

song_ignore = ['search_rank','tracks','audio_md5']
analysis_ignore = ['bars','segments','track','beats','meta',
    'sections','tatums','audio_md5']
audio_summary_ignore = ['audio_md5']

def read_songs():
    for line in fileinput.input():
        yield ujson.loads(line)

def strip_dict(d,trash):
    for field in trash:
        if field in d:
            del d[field]
            
seen  = set()

def prune_songs(songs):
    pruned_songs = []
    for song in songs:
        #print song['id']
        stripped_song = song
        if stripped_song['id'] in seen:
            continue
        strip_dict(stripped_song, song_ignore)
        strip_dict(stripped_song['analysis'], analysis_ignore)
        strip_dict(stripped_song['audio_summary'], audio_summary_ignore)
        seen.add(stripped_song['id'])
        pruned_songs.append(stripped_song)
    return pruned_songs

def reorg_songs(songs):
    clean_songs = []
    for song in songs:
        clean_song = {}
        clean_song['title'] = song['title']
        clean_song['artist_name'] = song['artist_name']
        clean_song['energy'] = song['audio_summary']['energy']
        clean_song['tempo'] = song['audio_summary']['tempo']
        clean_song['speechiness'] = song['audio_summary']['speechiness']
        clean_song['key'] = song['audio_summary']['key']
        clean_song['duration'] = song['audio_summary']['duration']
        clean_song['liveness'] = song['audio_summary']['liveness']
        clean_song['mode'] = song['audio_summary']['mode']
        clean_song['time_signature'] = song['audio_summary']['time_signature']
        clean_song['loudness'] = song['audio_summary']['loudness']
        clean_song['danceability'] = song['audio_summary']['danceability']
        clean_songs.append(clean_song)

    return clean_songs
        
        
        
        

if __name__ == "__main__":
    songs = read_songs()
    pruned_songs = prune_songs(songs)
    data_file = open("nice_data.json", 'w')
    ujson.dump(pruned_songs, data_file, indent=4)
    
    
