import csv
import os, shutil
import subprocess
from pathlib import Path

#TODO inserire il percorso in cui si trova lo script come d'esempio:
path = R'C:\Users\Lara\Documents\Universita\TerzoAnno\IntroduzioneIA\Progetto'

#API di Spotify per scrivere le tracce su file csv
#TODO rimuovere questa funzione in caso di problemi con le API
def track_generation():
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    with open('tracks.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['trackID','track_name','artistID'])
        for track in sp.playlist_tracks("https://open.spotify.com/playlist/7IKp6J4FFOGND94z7nYH0V?si=67820d422aef4c01")["items"]:
            track_uri = track["track"]["uri"]
            splitted = track_uri.split(":")
            track_uri = splitted[2]
            track_name = track["track"]["name"]
            artist_uri = track["track"]["artists"][0]["uri"]
            splitted = artist_uri.split(":")
            artist_uri = splitted[2]
            writer.writerow([track_uri,track_name,artist_uri])
track_generation()

#controlla che il file di output dell'RMLStreamer non esista, altrimenti lo elimina
if os.path.isdir("OutputMapping"):
    shutil.rmtree("OutputMapping")
#RMLStreamer con file
returned_value = subprocess.call('java --add-opens java.base/java.util=ALL-UNNAMED -jar RMLStreamer-v2.5.0-standalone.jar toFile --mapping-file ' + path + 
                                 '\\MusicMapping.ttl --output-path ' + path + '\\OutputMapping', shell=True)
#riformattazione sull'output di RMLStreamer
for count in range(1,9):
    p = Path(path + '\\OutputMapping\\' + str(count))
    p.rename(p.with_suffix('.ttl'))
filenames = [path + '\\OutputMapping\\1.ttl',
             path + '\\OutputMapping\\2.ttl',
             path + '\\OutputMapping\\3.ttl',
             path + '\\OutputMapping\\4.ttl',
             path + '\\OutputMapping\\5.ttl',
             path + '\\OutputMapping\\6.ttl',
             path + '\\OutputMapping\\7.ttl',
             path + '\\OutputMapping\\8.ttl']
with open('output.ttl', 'w') as outfile:
    for names in filenames:
        with open(names) as infile:
            outfile.write(infile.read())
#query con SPARQL
print("Il tuo artista preferito è:")
returned_value = subprocess.call('comunica-sparql-file ' + path + 
                                 R'\output.ttl "PREFIX mo: <http://purl.org/ontology/mo/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> ' +
                                 'SELECT (SAMPLE(?a) AS ?URI) (SAMPLE(?n) AS ?ARTIST_NAME) (COUNT(?t) as ?NUM_SONGS) ' +
                                 'WHERE {?a a mo:MusicArtist . ?t mo:MusicArtist ?a . ?a foaf:name ?n} GROUP BY ?a ORDER BY DESC (?NUM_SONGS) LIMIT 1"', shell=True)
print("Artisti consigliati per genere musicale...")
returned_value = subprocess.call('comunica-sparql-file ' + path + 
                                 R'\output.ttl "PREFIX mo: <http://purl.org/ontology/mo/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX db: <http://dbpedia.org/>' +
                                 'SELECT ?url ?name WHERE{ ?url a mo:MusicArtist . ?url db:MusicGenre ?MUSIC_GENRE. ?url foaf:name ?name. ' +
                                 '{SELECT (SAMPLE(?a) AS ?URI) (SAMPLE(?n) AS ?ARTIST_NAME) (SAMPLE(?g) AS ?MUSIC_GENRE) (COUNT(?t) as ?NELEMENTS) ' + 
                                 'WHERE {?a a mo:MusicArtist . ?t mo:MusicArtist ?a . ?a foaf:name ?n . ?a db:MusicGenre ?g} GROUP BY ?a ORDER BY DESC (?NELEMENTS) LIMIT 1}}"', 
                                 shell=True)
print("Artisti consigliati per nazionalità...")
returned_value = subprocess.call('comunica-sparql-file ' + path + 
                                 R'\output.ttl "PREFIX mo: <http://purl.org/ontology/mo/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX db: <http://dbpedia.org/> ' +
                                 'SELECT ?url ?name WHERE{ ?url a mo:MusicArtist . ?url db:Country ?COUNTRY. ?url foaf:name ?name. ' +
                                 '{SELECT (SAMPLE(?a) AS ?URI) (SAMPLE(?n) AS ?ARTIST_NAME) (SAMPLE(?g) AS ?COUNTRY) (COUNT(?t) as ?NELEMENTS) ' +
                                 'WHERE {?a a mo:MusicArtist . ?t mo:MusicArtist ?a . ?a foaf:name ?n . ?a db:Country ?g} GROUP BY ?a ORDER BY DESC (?NELEMENTS) LIMIT 1}}"', shell=True)
print("Artisti consigliati per la tua età...")
returned_value = subprocess.call('comunica-sparql-file ' + path + 
                                 R'\output.ttl "PREFIX mo: <http://purl.org/ontology/mo/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX rml-io: <https://kg-construct.github.io/rml-io/ontology/documentation/index-en.html#http://w3id.org/> ' +
                                 'SELECT ?url ?name WHERE{ ?url a mo:MusicArtist . ?url rml-io:Target ?TARGET. ?url foaf:name ?name. ' +
                                 '{SELECT (SAMPLE(?a) AS ?URI) (SAMPLE(?n) AS ?ARTIST_NAME) (SAMPLE(?g) AS ?TARGET) (COUNT(?t) as ?NELEMENTS) ' +
                                 'WHERE {?a a mo:MusicArtist . ?t mo:MusicArtist ?a . ?a foaf:name ?n . ?a rml-io:Target ?g} GROUP BY ?a ORDER BY DESC (?NELEMENTS) LIMIT 1}}"', shell=True)