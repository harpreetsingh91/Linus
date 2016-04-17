'''run this file once to calculate vectors for songs and save them in a file'''
import ast
from tables import *
import numpy as np
import json
import pickle


#read median values
'''this is a new file for calculatiing vectors based on timbre values plus values used earlier'''
f = open("savedFiles/medianValues.txt", 'r')
fa = f.read()
fa = ast.literal_eval(fa)
loudnessMedian = float(fa['loudness'])
#we won't use hotness this time
tempoMedian = float(fa['tempo'])
songKeyMedian = float(fa['songKey'])
f.close() #close file f
medianTimbres = [43.35208806,6.57995769,12.76659855,0.16575301,-2.71059666] #can be read from file but hardcoded here
songVectorData = {}
count = -1 #this will ensure count starts from zero and adjacencyMatrix and vector has same number for song
#perform one time calculation to create vector for each song. Save it in file to save time

#creating an instance of linusUtilities class

from utilities import linusUtilities

utilV = linusUtilities()

def songVectorGeneratorNew(filename):
    global count, songVectorData
    count += 1 #just to give a number to the song
    songVector = np.array([])
    vectorValueTempo = 0
    vectorValueLoudness = 0
    vectorValueSongKey = 0
    vectorValueTimbre1 = 0
    vectorValueTimbre2 = 0
    vectorValueTimbre3 = 0
    vectorValueTimbre4 = 0
    vectorValueTimbre5 = 0
    h5 = util.GETTERS.open_h5_file_read(filename)
    #vector is like this [tempo, loudness, mode, songKey, and then the timbres]
    if (util.GETTERS.get_tempo(h5) > tempoMedian):
        vectorValueTempo = 2
    if (util.GETTERS.get_loudness(h5) > loudnessMedian):
        vectorValueLoudness = 1
    if (util.GETTERS.get_key(h5) >= songKeyMedian):
        vectorValueSongKey = 1

    #timbres below

    timbre = np.array(util.GETTERS.get_segments_timbre(h5))
    means = timbre.mean(axis=0) #this gets mean values of timbre values for each song
    # now compare mean of this song to overall median values for timbres of 10,000 songs
    if (means[0]>medianTimbres[0]):
        vectorValueTimbre1 = 1

    if (means[1]>medianTimbres[1]):
        vectorValueTimbre2 = 1

    if (means[2]>medianTimbres[2]):
        vectorValueTimbre3 = 1

    if (means[3]>medianTimbres[3]):
        vectorValueTimbre4 = 1

    if (means[4]>medianTimbres[4]):
        vectorValueTimbre5 = 1

    vectorValueMode = int((util.GETTERS.get_mode(h5))) #since mode is alreay in 0,1 form
    songVector = np.array([vectorValueTempo, vectorValueLoudness, vectorValueMode, vectorValueSongKey, vectorValueTimbre1, vectorValueTimbre2, vectorValueTimbre3, vectorValueTimbre4, vectorValueTimbre5])
    songVectorData[count] = tuple((util.GETTERS.get_song_id(h5),songVector.tolist()))#adding new value to the songVectorData dictionary
    h5.close()
    #arrays converted to lists so that they can be saved to a file
util.apply_to_all_files(util.msd_subset_data_path,func=songVectorGeneratorNew) #function called to apply songVectorGenerator function on complete dataset

#now write songVectorData to file
json.dump(songVectorData, open("savedFiles/songVectorsFileJSONwithTimbres.txt", 'w'))
#code above was run to create the songVectorsFile and since it won't be changing
#it has been written to disk and for future use it be read from there.
