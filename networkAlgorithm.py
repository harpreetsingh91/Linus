import ast
from tables import *
import numpy as np

from utilities import linusUtilities

utilNW = linusUtilities()
# imports specific to the MSD
import json
import pickle
from operator import itemgetter
# we define the function to apply to all files

class linusAlgorithm(object):


    readVectorFile = json.load(open("savedFiles/songVectorsFileJSONwithTimbres.txt"))

    #no need to actually create an advanced playlist. Just play n nearest neigbors
    #to the seedSong

    h5File = open_file('savedFiles/adjacencyMatrixWithTimbres.hdf', 'r', title = "test file")

    abc = h5File.root.adjacencyMatrix

    #seedSong0 = "SOBLGCN12AB0183212" # just for testing. seedSong is actually assigned from mobile app

    #readVectorFile contains a dictionary with key as number of song

    def __init__(self):
        self.closest = []
        self.seedSong0 = "SOBLGCN12AB0183212"


    def setSeedSong(self, seedSong):
        xyz = self.abc[:1000,:1000]
        self.seedSong0 = seedSong
        #code below gets number of song from Vector file
        for i in range(0,10000):
            if self.readVectorFile[str(i)][0] == seedSong:
                songNumber = i
                break


        print songNumber
        # songNumber +1 is song number in our vector dictionary.
        # songNumber is subtracted by one above since adjacencymatrix starts at 0

        counter = 0
        for i in self.abc[songNumber]:
            if i==0 and counter!= songNumber: #this avoids adding the seed to the playlist
                self.closest += [(counter,i, str(self.readVectorFile[str(counter)][0]))]
            counter += 1

        #print closest
        print "the song Id here is"+seedSong

        songIDs = []
        for i in self.closest:
            songIDs += [i[2]]


    #first playlist is the N closest neigbors of seedSong

    # play the five songs. Consider likes and dislikes based on these songs

    # implement heuristic D as given in

    #http://cis.ofai.at/~elias.pampalk/publications/pam_ismir05b.pdf

    '''use format below. This is just to test'''
    #linusMasala = {'liked':['SONYPOM12A8C13B2D7', 'SOYQOFI12A6D4F76E1', 'SODLSHA12AAF3B29F2', 'SOEBDBO12AC4688712'], 'disliked':['SOOCWAO12AB01852C1', 'SOGIAKH12AB0184D05', 'SOJBWGF12A8159E883', 'SOFJWKK12AB01826CD']} #linusMasala maintains

    ''''''

    # look at list of candidate songs.
    # Da = distance to nearest accepted, Ds is distance to nearest skipped
    # If Da < Ds then add candidate to set S
    # From S play song with smallest Da
    # If S is empty, then play song with best Da/Ds ratio

    # linusCurryMaker returns one song at a time. Will be called again and again as likes and dislikes keep coming

    #code below gets number of song from Vector file
    def getNumberInVectorFile(self, song):
        for i in range(0,10000): # changed from 1,10001
            if self.readVectorFile[str(i)][0] == song:
                songNumber = i
                #print "eh chako song"+song
                #break
                return songNumber

     # to get 2nd item in tuple to sort it by that element
    #def calculateDistance(inputx, liked = linusMasala['liked'], disliked = linusMasala['disliked']):
    def calculateDistance(self, inputx, liked, disliked):
        #this function calculates distance from liked and disliked songs
        distances = {} # list of tuples (i,closest liked song, closes disliked song)
        for i in range(1,inputx):
            iData = self.readVectorFile[str(i)][1] #since vector data is at position 1
            likedSongsDistances = []
            dislikedSongsDistances = []

            for j in liked:
                likedSongNumber = self.getNumberInVectorFile(j)
                jData = self.readVectorFile[str(likedSongNumber)][1]
                temp = sum(abs(np.array(iData)-np.array(jData)))
                likedSongsDistances.append(tuple((j,temp)))
            for k in disliked:
                dislikedSongNumber = self.getNumberInVectorFile(j)
                kData = self.readVectorFile[str(dislikedSongNumber)][1]
                temp = sum(abs(np.array(iData)-np.array(kData)))
                dislikedSongsDistances.append(tuple((j,temp)))
            likedSongsDistances.sort(key=itemgetter(1))
            dislikedSongsDistances.sort(key=itemgetter(1))
            #now append distance to closest liked song and closest disliked song with the song i
            distances[i] = tuple((likedSongsDistances[0],dislikedSongsDistances[0]))
        return distances


    def linusCurryMaker(self, inputx, linusMasala):
        #for each candidate song i.e unplayed song calculate distance from liked and disliked
        #choose song that has smallest Da and has Da>Ds
        xDistances = self.calculateDistance(inputx, linusMasala['liked'], disliked = linusMasala['disliked'])
        validSongs = []
        for i in xDistances:
            if xDistances[i][0][1]<xDistances[i][1][1]:
                validSongs.append(tuple((i,xDistances[i][0][1])))
        #print validSongs
        validSongs.sort(key=itemgetter(1))
        if len(validSongs) == 0:
            for i in xDistances:
                if xDistances[i][1][1] > 0:
                    validSongs.append(tuple((i,xDistances[i][0][1]/xDistances[i][1][1])))
            validSongs.sort(key=itemgetter(1))
        return validSongs[:10]
