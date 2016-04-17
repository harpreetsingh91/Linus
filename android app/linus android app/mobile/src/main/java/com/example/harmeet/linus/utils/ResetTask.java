package com.example.harmeet.linus.utils;

import android.os.AsyncTask;
import android.util.Log;

import com.example.harmeet.linus.beans.Song;
import com.example.harmeet.linus.logic.SongsManager;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Ishmeet on 10/04/16.
 */
public class ResetTask extends AsyncTask<String, Void, String> {

    SongsManager songsManager;
    RestClient restClient;

    public ResetTask(SongsManager songsManager) {
        this.songsManager = songsManager;
        this.restClient = new RestClient();
    }

    protected String doInBackground(String... urls) {
        String urldisplay = urls[0];
        String result = null;
        try {
            result = restClient.requestContent(urldisplay);
        } catch (Exception e) {
            Log.e("Error", e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    protected void onPostExecute(String result) {
        ArrayList<Song> songList = new Gson().fromJson(result, new TypeToken<ArrayList<Song>>(){}.getType());
        ArrayList<HashMap<String,String>> songMapList = new Gson().fromJson(result, new TypeToken<ArrayList<HashMap<String,String>>>(){}.getType());
        songsManager.setSongList(songList);
        songsManager.setSongMapList(songMapList);
    }
}