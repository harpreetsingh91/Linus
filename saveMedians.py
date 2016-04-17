'''run this file once to save median values for the dataset in a text file'''

import numpy as np

from utilities import linusUtilities

util = linusUtilities()


hotnessValues = np.array([])
tempoValues = np.array([])
loudnessValues = np.array([])
modeValues = np.array([])
keyValues = np.array([])
#returnMedianValues for energy, speechiness, tempo, danceability
def returnMedianValues(filename):
    global hotnessValues, tempoValues, loudnessValues, modeValues, keyValues
    #set as global because otherwise python tries to create a local variable inside function
    h5 = util.GETTERS.open_h5_file_read(filename) #this stores the file in h5 variable
    songHotness = util.GETTERS.get_song_hotttnesss(h5)
    songTempo = util.GETTERS.get_tempo(h5)
    songLoudness = util.GETTERS.get_loudness(h5)
    songMode = util.GETTERS.get_mode(h5)
    songKey = util.GETTERS.get_key(h5)
    if (songHotness > 0.0):
        hotnessValues = np.append(hotnessValues, songHotness)

    tempoValues = np.append(tempoValues,songTempo)
    loudnessValues = np.append(loudnessValues, songLoudness)
    modeValues = np.append(modeValues, songMode)
    keyValues = np.append(keyValues, songKey)
    h5.close()

#from old values don't use hotnessValues as it is not very relevant.
timbres = []

def returnMedianValues2(filename):
    global timbres #setting as global so that the values can be altered from within function
    h5 = util.GETTERS.open_h5_file_read(filename) #this stores the file in h5 variable
    timbre = np.array(util.GETTERS.get_segments_timbre(h5))

    means = timbre.mean(axis=0)
    timbres.append([means[0],means[1],means[2],means[3],means[4]])
    h5.close()

#apply_to_all_files(msd_subset_data_path,func=returnMedianValues)
util.apply_to_all_files(util.msd_subset_data_path,func=returnMedianValues2)

#now find median values in the timbres list

timbres = np.array(timbres)

medianTimbres = list(np.median(timbres, axis =0))

#next time save in a format that is not numpy array since it can't be read properly from text file

saveToFileX = open("/savedFiles/medianTimbreValues.txt", "w")
saveToFileX.write(str(medianTimbres))
saveToFileX.close()
