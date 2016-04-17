import networkAlgorithm as tadka
from flask import Flask
#from flask import render_template
import json
import urllib
from flask import request
import requests

linusAlgoObject = tadka.linusAlgorithm()

app = Flask(__name__)

readVectorFile = json.load(open("savedFiles/songVectorsFileJSONwithTimbres.txt"))
readSongsInfoFile = json.load(open("savedFiles/SongsAndArtists.txt"))

url = 'http://developer.echonest.com/api/v4/song/search?'

data = {}
data['api_key'] = 'removedKey'; #todo remove key before posting online
data['format'] = 'json';
data['results'] = '1';
data['bucket'] = ['id:7digital-US','id:spotify','tracks'];
data['limit'] = 'true';


testMasala = {}

songNames = []


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
    if spotifyUri == None: #or thumbnail==None:
        return None
    return {'echonestId':echoSongID,'artist':artistName,'name':songName,'uri':spotifyUri,'thumbnail':thumbnail}

#testMasala = {'disliked':'SOBLGCN12AB0183212'}

testMasala = {'liked':[],'disliked':[]}

firstDislike = True
firstLike = True

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
    #print str(readSongsInfoFile[linusAlgoObject.seedSong0][0])
    #print str(readSongsInfoFile[linusAlgoObject.seedSong0][1])
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

@app.route("/reset")
def reset():
    testMasala['liked'] = []
    testMasala['disliked'] = []
    return "reset"

if __name__ =='__main__':
	app.run(host = "localhost", port = 8080, debug = True)
    #app.run(host = '0.0.0.0', port = 8080, debug = False)
