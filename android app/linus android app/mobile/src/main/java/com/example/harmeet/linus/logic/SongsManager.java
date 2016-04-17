package com.example.harmeet.linus.logic;

/**
 * Created by Harmeet on 2016-04-09.
 */

import android.os.Parcelable;

import com.example.harmeet.linus.beans.Song;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class SongsManager implements Serializable{
    String jsonString = "[{\"name\":\"Often\",\"artist\":\"The Weekend\",\"thumbnail\":\"https://i.scdn.co/image/51a60fbb7daba6e6fbc0d3b47e34017dce6f3921\",\"uri\":\"spotify:track:5SqSckut3FcoQKmGkMWgp1\"},{\"name\":\"stan\",\"artist\":\"Eminem\",\"thumbnail\":\"https://i.scdn.co/image/135ffbfeb47d564df36fdb4756c070b3ac32cd3b\",\"uri\":\"spotify:track:3UmaczJpikHgJFyBTAJVoz\"},{\"name\":\"Stay\",\"artist\":\"Kygo\",\"thumbnail\":\"https://i.scdn.co/image/9680cd709838a5ba5a2118e018e0ae2edf4f24f7\",\"uri\":\"spotify:track:7gBj0VgcuAgkXkiRRYvSmK\"},{\"name\":\"Paradise\",\"artist\":\"Coldplay\",\"thumbnail\":\"https://i.scdn.co/image/e7a649b3890dc849e0f1597d6d12b4342e03ce5f\",\"uri\":\"spotify:track:6nek1Nin9q48AVZcWs9e9D\"},{\"name\":\"Hello\",\"artist\":\"Adele\",\"thumbnail\":\"https://i.scdn.co/image/f71517e8919892273de8d8677e42cdcf1b976aa7\",\"uri\":\"spotify:track:0ENSn4fwAbCGeFGVUbXEU3\"},{\"name\":\"Lollipop\",\"artist\":\"Lil Wayne\",\"thumbnail\":\"https://api.spotify.com/v1/albums/5BGzOpea6At0Nd7tYtYZOP\",\"uri\":\"spotify:track:4P7VFiaZb3xrXoqGwZXC3J\"}]";
    ArrayList<Song> songList;
    int songIndex;

    public SongsManager(){
        songList = new Gson().fromJson(jsonString, new TypeToken<ArrayList<Song>>(){}.getType());
        songIndex = 0;
    }

    public Song getCurrentSong() {
        return songList.get(songIndex);
    }

    public Song getNextSong() {
        songIndex++;
        return songList.get(songIndex);
    }

    public ArrayList<HashMap<String,String>> getSongMapList() {
        return new Gson().fromJson(jsonString, new TypeToken<ArrayList<HashMap<String,String>>>(){}.getType());
    }

}
