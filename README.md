# Linus
#Linus Music Recommendation System

###Just a short summary of the application. I will add a more detailed description of the application later

* networkAlgorithm.py contains the main algorithm

* linusServer.py contains the server implementation

* utilities.py contains functions that will be used often

* Android app folder contains the mobile app for this application. Credits to IshmeetKohli and HarmeetSaimbhi for contributing to the app.

Most of the other .py files are run once to get features/info from songs database. This data is stored in files and is read from there.

**TODO:**

Provide more explanation for the server and app communication process.

In short, app calls "first" function when it is run for the first time. For every call after the first one,
"later" function is called. (TODO part: simplify this)

###Process:

* Million song dataset was used for getting audio features.

* The whole dataset was read and features for each song were averaged out over the entire song duration.

* A median value was calculated for each feature of the songs in the dataset.

* If the value of feature of a song falls below the median it was given a value of 0 and if it was greater than or equal to the median it was given a value of 1.

* After tweaking and playing with the dataset it was decided to give greater weight to tempo of the song.

* After this step we had the vector representations of each song in the dataset.

* This was used to calculate distance between songs and an adjacency matrix was created. The distance formula used was a simple difference between the two vectors and an absolute value was taken to avoid negative distances. We avoided float values as they create a very big file.

* HDF5 format was used for storing data as this provides a fast and efficient way to store a large amount of data.

* The main algorithm for calculating distance from liked and disliked songs was written. Basically, if a song is closer to a liked song than it is to a disliked song, then it is a valid candidate song. If there are no valid candidate songs, we take into account ratios. The song closest to one of the liked songs is chosen to be played next i.e. the song with the smallest liked distance/disliked distance ratio.

* The algorithm is imported and run as a Flask server which interacts with the mobile app through http services. Flask server takes in parameters from app and returns a json file containing information about the next song to be played.

#### Future scope:

1. Since this is a basic working prototype, the foremost thing to do is provide performance improvements so that
   the application can be scaled.

2. Better way to represent song vectors. Instead of just binary vectors, use a range of values.

3. Introduce Genre feature and a test a better algorithm to calculate distances.

4. Provide a more detailed documentation.