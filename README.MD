# Spotify Stats Creator

A script that creates your Spotify Statistics analyzing your parsed [streaming history](https://www.spotify.com/us/account/privacy/).  


## Getting started
- Run the [HistoryParser](https://github.com/Chareste/SpotifyHistoryParser) or the [ExtendedHistoryParser](https://github.com/Chareste/SpotifyHistoryParserExtended)
- Install the required dependencies
- Download *statsCreator.py* and place it in the parser's root folder.

### Dependencies

You will need to install [plotext](https://github.com/piccolomo/plotext) and [numPy](https://numpy.org/) to make it work.  
Just run these in your terminal:

```
pip install plotext
pip install numpy
```
## Running the program
Open the terminal and move into your root folder. Then run *statsCreator.py* with Python with this command:  
```
python3 statsCreator.py
```
Or, if you're on windows:
```
python statsCreator.py
```

## Output

You will get a text file called *out.txt*, containing the effective output of the program, 
and two new JSON files in the out folder, *tracksData.json* and *artistsData.json*.  
If you ran the Extended parser, *showsData.json* will be created too.

### out.txt

This file will provide you the following informations:
- Total HH:MM:SS of listening and equivalent day number
- How popular your tracks are
- A graph with your listens by hour
- Top 100 of the most played songs
  - number of plays
  - total HH:MM:SS
  - average number of plays based on ms played and the song length
  - How popular is the track
  - Time of the day when it was most played
- Top 50 of the most played artists
  - number of plays
  - total HH:MM:SS
  - Time of the day when it was most played
  - Top 5 most played songs with number of plays
- (Extended only) Top 10 of the most played shows
  - Number of episodes played
  - total HH:MM:SS
  - Time of the day when it was most played

### tracksData.json

It contains all the tracks listened in order of number of plays.

#### Structure
```
{
  TRACK_POSITION: {
    "ID": TRACK_ID,
    "Artist": ARTIST_NAME,
    "Title": TRACK_NAME,
    "msDuration": LENGTH_IN_MILLISECONDS,
    "TimesPlayed": TIMES_PLAYED>=1/3_TRACK_LEN,
    "msPlayed": TOTAL_MILLIS_PLAYED
    "timeDistribution": [ PLAYS_PER_3HR_BLOCKS ]
  },
  [...]
}
```
### artistsData.json

Contains all the artists in order of number of plays.

#### Structure
```
{
  ARTIST_NAME: {
    "Position": ARTIST_POSITION
    "totalMillis": TOTAL_MILLIS_PLAYED,
    "totalListens": TOTAL_TIMESPLAYED_FOR_ARTIST,
    "Tracks": {
      TRACK_NAME: {
        "ID": TRACK_ID,
        "TimesPlayed": TIMES_PLAYED>=1/3_TRACK_LEN
      },
      [...]
    }
    "timeDistribution": [ PLAYS_PER_3HR_BLOCKS ]
  },
  [...]    
}  
```
### showsData.json
It contains all the shows listened in order of number of episodes played.
### Structure
```
{
  SHOW_POSITION: {
    "ID": SHOW_ID,
    "Show": SHOW_NAME,
    "Publisher": PUBLISHER_NAME,
    "totalEpisodes": TOTAL_EPISODES,
    "totalMillis": TOTAL_MS_PLAYED,
    "totalPlayed": TOTAL_EPISODES_PLAYED,
    "playedEpisodes":{
      EPISODE_ID:{ "Name": EPISODE_NAME }
      [...]
    }
    "timeDistribution": [ PLAYS_PER_3HR_BLOCKS ]
  },
  [...]
}
```
## Known issues

### Podcast episodes - yearly parser
The program may display incorrect data when encountering a podcast episode. Unfortunately it doesn't seem to be fixable 
because it's impossible to discern them from tracks based on the given data.  
This is not an issue if you ran the extended parser.


