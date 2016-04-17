# usual imports
import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np # get it at: http://numpy.scipy.org/
# path to the Million Song Dataset subset (uncompressed)
# CHANGE IT TO YOUR LOCAL CONFIGURATION

class linusUtilities(object):
    msd_subset_path='/Users/harpreetsingh/Downloads/MillionSongSubset'
    msd_subset_data_path=os.path.join(msd_subset_path,'data')
    msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
    assert os.path.isdir(msd_subset_path),'wrong path' # sanity check
    # path to the Million Song Dataset code
    # CHANGE IT TO YOUR LOCAL CONFIGURATION
    msd_code_path='/Users/harpreetsingh/Google Drive/Uvic Assignments and work/MIR/project/Linus/Code/imports/MSongsDB'
    assert os.path.isdir(msd_code_path),'wrong path' # sanity check
    # we add some paths to python so we can import MSD code
    # Ubuntu: you can change the environment variable PYTHONPATH
    # in your .bashrc file so you do not have to type these lines
    sys.path.append( os.path.join(msd_code_path,'PythonSrc') )

    print "yes"

    def __init__(self):
        self.songNameAndArtist = []
        import hdf5_getters as GETTERS
        self.GETTERS = GETTERS

    # the following function simply gives us a nice string for
    # a time lag in seconds
    def strtimedelta(starttime,stoptime):
        return str(datetime.timedelta(seconds=stoptime-starttime))

    def apply_to_all_files(self, basedir,func=lambda x: x,ext='.h5'):
        """
        From a base directory, go through all subdirectories,
        find all files with the given extension, apply the
        given function 'func' to all of them.
        If no 'func' is passed, we do nothing except counting.
        INPUT
           basedir  - base directory of the dataset
           func     - function to apply to all filenames
           ext      - extension, .h5 by default
        RETURN
           number of files
        """
        cnt = 0
        # iterate over all files in all subdirectories
        for root, dirs, files in os.walk(basedir):
            files = glob.glob(os.path.join(root,'*'+ext))
            # count files
            cnt += len(files)
            # apply function to all files
            for f in files :
                func(f)
        return cnt


    def func_to_get_songNameAndArtist(self, filename):
        """
        This function does 3 simple things:
        - open the song file
        - get title and artist name
        - append it as a tuple to the songNameAndArtist list
        - close the file
        """
        h5 = self.GETTERS.open_h5_file_read(filename)
        songTemp = self.GETTERS.get_title(h5)
        artistTemp = self.GETTERS.get_artist_name(h5)
        self.songNameAndArtist.append(tuple((songTemp,artistTemp)))
        h5.close()
