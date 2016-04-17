package com.example.harmeet.linus.activity;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import com.example.harmeet.linus.R;
import com.example.harmeet.linus.beans.Song;
import com.example.harmeet.linus.logic.SongsManager;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;

public class PlayListActivity extends ListActivity {

    SongsManager songsManager;
    ArrayList<HashMap<String, String>> songMapList;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.playlist);
        Intent intent = getIntent();

        songMapList = (ArrayList<HashMap<String, String>>) intent.getSerializableExtra("songMapList");

        ListAdapter adapter = new SimpleAdapter(this, songMapList, R.layout.playlist_item, new String[]{"name","artist"}, new int[]{R.id.songTitle,R.id.songArtist});
        setListAdapter(adapter);
    }


}
