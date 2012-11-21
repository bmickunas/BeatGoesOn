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
    for song in songs:
        if song['id'] in seen:
            continue
        strip_dict(song, song_ignore)
        strip_dict(song['analysis'], analysis_ignore)
        strip_dict(song['audio_summary'], audio_summary_ignore)
        seen.add(song['id'])
    return songs