Recommender.py è un progettino didattico nato come esempio d'uso di RML, linguaggio di mapping di RDF, utilizzando alcuni tools forniti da RML.io.
è uno script in Python che:
- Tramite Spotipy, API di Spotify per Python, preleva le tracce contenute di una playlist e ne trascrive alcune informazioni (id della traccia, titolo ed id dell'artista musicale ad essa collegata) su un file .csv, chiamato "tracks.csv"
- Tramite le regole specificate nel file "MusicMapping.ttl", effettua il mapping dalle sorgenti "tracks.csv" e "artist.json". Per farlo utilizza RMLStreamer che, in questo caso, fornisce in output tramite file le triple RDF generate.
- Dopo aver riformattato correttamente il file output di RMLStreamer, viene utilizzato Comunica per effettuare delle query SPARQL, risultati delle quali vengono stampati e rappresentano nomi ed url di artisti musicali consigliati sulla base delle tracce presenti nella playlist iniziale.

Setup del progetto:
- Nella cartella del progetto, oltre ai file presenti su git, occorre inserire il file 'RMLStreamer-v*.*.*-standalone.jar' scaricabile qui: https://github.com/RMLio/RMLStreamer/releases/tag/v2.5.0
- Inserire il percorso della cartella di progetto e la versione di RMLStreamer nello script 'recommender.py' come indicato da commenti direttamente nel file
Setup Spotipy:
- Installare i package necessari:
	pip install spotipy --upgrade
- Al primo avvio, le API di Spotify potrebbero chiedere di inserire un URL, in caso copiare ed incollare a terminale l'URL a cui si viene direttamente reinderizzati
- In caso ci fossero problemi con le API di Spotify, è già presente un esempio di file generato (tracks.csv), per cui si può rimuovere la parte di progetto correlata come indicato direttamente nello script.
Setup Comunica:
- Installare Comunica come indicato qui: https://comunica.dev/docs/query/getting_started/query_cli/
