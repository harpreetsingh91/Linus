package com.example.harmeet.linus.logic;

import android.content.Intent;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;

import com.example.harmeet.linus.R;
import com.example.harmeet.linus.activity.MainActivity;
import com.example.harmeet.linus.activity.PlayListActivity;
import com.example.harmeet.linus.beans.Song;
import com.example.harmeet.linus.utils.DownloadImageTask;
import com.example.harmeet.linus.utils.Utilities;
import com.spotify.sdk.android.player.PlayerState;
import com.spotify.sdk.android.player.PlayerStateCallback;

/**
 * Created by Ishmeet on 10/04/16.
 */
public class ActionHandler implements SeekBar.OnSeekBarChangeListener {

    public static final int STATE_STOPPED = 0;
    public static final int STATE_PLAYING = 1;
    public static final int STATE_PAUSED = 2;

    MainActivity activity;
    SongsManager songsManager;

    private ImageButton btnPlay;
    private ImageButton btnLike;
    private ImageButton btnDislike;
    private ImageButton btnPlaylist;

    private SeekBar songProgressBar;

    private TextView songTitleLabel;
    private TextView songArtistLabel;
    private TextView songCurrentDurationLabel;
    private TextView songTotalDurationLabel;

    private ImageView albumArt;

    private int state;
    private Handler mHandler;

    private Utilities utils;

    public ActionHandler(MainActivity activity, SongsManager songsManager) {
        this.activity = activity;
        this.songsManager = songsManager;
        state = STATE_STOPPED;
        mHandler = new Handler();
        utils = new Utilities();

        //All buttons
        btnPlay = (ImageButton) activity.findViewById(R.id.btnPlay);
        btnLike = (ImageButton) activity.findViewById(R.id.btnLike);
        btnDislike = (ImageButton) activity.findViewById(R.id.btnDislike);
        btnPlaylist = (ImageButton) activity.findViewById(R.id.btnPlaylist);
        albumArt = (ImageView) activity.findViewById(R.id.albumArt);

        songProgressBar = (SeekBar) activity.findViewById(R.id.songProgressBar);
        songTitleLabel = (TextView) activity.findViewById(R.id.songTitle);
        songArtistLabel = (TextView) activity.findViewById(R.id.songArtist);
        songCurrentDurationLabel = (TextView) activity.findViewById(R.id.songCurrentDurationLabel);
        songTotalDurationLabel = (TextView) activity.findViewById(R.id.songTotalDurationLabel);

        setListeners();
        songProgressBar.setOnSeekBarChangeListener(this);
    }

    public void setListeners() {

        btnPlay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {

                switch (state) {
                    case STATE_STOPPED:
                        playSong(songsManager.getCurrentSong());
                        btnPlay.setImageResource(R.drawable.btn_pause);
                        state = STATE_PLAYING;
                        break;
                    case STATE_PLAYING:
                        activity.getmPlayer().pause();
                        btnPlay.setImageResource(R.drawable.btn_play);
                        state = STATE_PAUSED;
                        break;
                    case STATE_PAUSED:
                        activity.getmPlayer().resume();
                        btnPlay.setImageResource(R.drawable.btn_pause);
                        state = STATE_PLAYING;
                        break;
                }
            }
        });

        btnLike.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                btnLike.setImageResource(R.drawable.img_btn_heart_pressed);
            }
        });

        btnDislike.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                playSong(songsManager.getNextSong());
                state = STATE_PLAYING;
                btnPlay.setImageResource(R.drawable.btn_pause);
            }
        });

        btnPlaylist.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                Intent intent = new Intent(activity.getApplicationContext(), PlayListActivity.class);
                intent.putExtra("songMapList",songsManager.getSongMapList());
                activity.startActivity(intent);
//                startActivityForResult(i, 100);
            }
        });
    }

    public void playSong(Song song) {
        activity.getmPlayer().play(song.getUri());
        songTitleLabel.setText(song.getName());
        songArtistLabel.setText(song.getArtist());
        new DownloadImageTask(albumArt).execute(song.getThumbnail());
        updateProgressBar();
    }


    public void updateProgressBar() {
        mHandler.postDelayed(mUpdateTimeTask, 100);
    }

    private Runnable mUpdateTimeTask = new Runnable() {
        public void run() {
            activity.getmPlayer().getPlayerState(new PlayerStateCallback() {
                @Override
                public void onPlayerState(PlayerState playerState) {
                    long totalDuration = playerState.durationInMs;
                    long currentDuration = playerState.positionInMs;

                    songTotalDurationLabel.setText(""+utils.milliSecondsToTimer(totalDuration));
                    songCurrentDurationLabel.setText(""+utils.milliSecondsToTimer(currentDuration));

                    int progress = (int)(utils.getProgressPercentage(currentDuration, totalDuration));
                    songProgressBar.setProgress(progress);
                }
            });

            mHandler.postDelayed(this, 100);
        }
    };

    @Override
    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {

    }

    @Override
    public void onStartTrackingTouch(SeekBar seekBar) {
        mHandler.removeCallbacks(mUpdateTimeTask);
    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar) {
        mHandler.removeCallbacks(mUpdateTimeTask);
        final int progress = seekBar.getProgress();

        activity.getmPlayer().getPlayerState(new PlayerStateCallback() {
            @Override
            public void onPlayerState(PlayerState playerState) {
                int totalDuration = playerState.durationInMs;
                int currentPosition = utils.progressToTimer(progress, totalDuration);
                activity.getmPlayer().seekToPosition(currentPosition);
            }
        });
        updateProgressBar();
    }
}