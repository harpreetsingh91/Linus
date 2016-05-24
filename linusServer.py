import networkAlgorithm as tadka
from flask import Flask

import json
import urllib
from flask import request
import requests

linusAlgoObject = tadka.linusAlgorithm()

app = Flask(__name__)

#read song vector data from file
readVectorFile = json.load(open("savedFiles/songVectorsFileJSONwithTimbres.txt"))

#read song info from file. This file has key value pairs of echonestId and (song name, artist name)
readSongsInfoFile = json.load(open("savedFiles/SongsAndArtists.txt"))

url = 'http://developer.echonest.com/api/v4/song/search?'

data = {}
data['api_key'] = 'U3TDA727EHDOFWS0G'; #todo remove key before posting online
data['format'] = 'json';
data['results'] = '1';
data['bucket'] = ['id:7digital-US','id:spotify','tracks'];
data['limit'] = 'true';

songNames = []

'''this function calls the spotify api and gets song information that is used to play the song on the mobile app
We can't use echonest song id to directly play songs on the spotify android sdk.
So we hit the spotify api with artist name and song name to get info that can be used to play the song on the app.
'''

def getSongMap(artistName,songName,echoSongID):
    data['artist'] = artistName;
    data['title'] = songName;
    url_values = urllib.urlencode(data,True);
    finalUrl =  url + url_values;
    apiResponse = requests.get(finalUrl)

    if not apiResponse.json()['response']['songs']:
        return None

    spotifyUri = None
    thumbnail = None
    for track in apiResponse.json()['response']['songs'][0]['tracks']:
        if track['catalog'] == 'spotify':
            spotifyUri = track['foreign_id']
        if track['catalog'] == '7digital-US':
            thumbnail = track['release_image']
    if spotifyUri == None:
        return None
    return {'echonestId':echoSongID,'artist':artistName,'name':songName,'uri':spotifyUri,'thumbnail':thumbnail}


#dictionary to store liked and disliked songs information
testMasala = {'liked':[],'disliked':[]}

firstDislike = True
firstLike = True


'''this function is supposed to be called when the app is run the first time. So, seed selection process
Pass the echonest song ID as a query parameter (argument name is 'first'), and set remark (argument name is 'remark') as 'liked'.
Since the first song is seed song chosen by user, it should be passed as liked.
A json is returned that contains information that can be played on the android app.

Multiple songs are returned in the json.

The returned package is an array of dictionaries. Each item is a dictionary representing song info.

Format :[{song1}, {song2},...]

Each song contained in package contains:
thumbnail, spotifyUri, echonestId, name of song, name of artist.

'''

@app.route("/first")
def first():
    songId = request.args.get('songId','')
    remark = request.args.get('remark','')
    a = request.args.get('songId','')
    testMasala[str(remark)] = [str(songId)]
    linusAlgoObject.setSeedSong(str(songId))

    print "This is songId"+songId
    print linusAlgoObject.closest[:10]

    print "nava maal"
    print linusAlgoObject.seedSong0

    firstSongs = [getSongMap(str(readSongsInfoFile[linusAlgoObject.seedSong0][0]),str(readSongsInfoFile[linusAlgoObject.seedSong0][1]),linusAlgoObject.seedSong0)]
    print testMasala

    count = 0
    for i in linusAlgoObject.closest[:10]:
        count+=1
        print count
        echoSongID= i[2]
        artistName = str(readSongsInfoFile[echoSongID][0])
        songName = str(readSongsInfoFile[echoSongID][1])
        songMap = getSongMap(artistName,songName,echoSongID)
        if(songMap != None):
            firstSongs.append(songMap)
    return json.dumps(firstSongs)


'''
after seed has been selected, every future call is to this function.

Usage of this function and data returned is similar to that of 'first' function call. But here remark can be passed based on response given by
user in the app.
'''

@app.route("/later")
def hello():
    songId = request.args.get('songId','')
    remark = request.args.get('remark','')
    testMasala[remark] += [str(songId)]
    print songId
    print remark
    print testMasala

    if len(testMasala)>0:
        suggestions = linusAlgoObject.linusCurryMaker(1001, testMasala)
        for i in suggestions:
            echoSongID = str(readVectorFile[str(i[0])][0])
            artistName = str(readSongsInfoFile[str(echoSongID)][0])
            songName = str(readSongsInfoFile[str(echoSongID)][1])
            songMap = getSongMap(artistName,songName,echoSongID)
            if echoSongID not in testMasala['liked'] and echoSongID not in testMasala['disliked'] and songMap!= None:
                songNames.append(songMap)
    return json.dumps([songNames[0]])

#song id SOXQTLK12AB018A1D9 is motherfucker. gives unicode error

#this empties the tadka dictionary. So new session doesn't rely on old likes and dislikes.
@app.route("/reset")
def reset():
    testMasala['liked'] = []
    testMasala['disliked'] = []
    return "reset"

if __name__ =='__main__':
	#app.run(host = "localhost", port = 8080, debug = True)
    app.run(host = '0.0.0.0', port = 8080, debug = False)
