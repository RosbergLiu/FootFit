package com.example.jiyuan.a;
import android.content.Intent;
import android.net.Uri;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.MemoryPolicy;
import com.squareup.picasso.NetworkPolicy;
import com.squareup.picasso.Picasso;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Heatmap extends AppCompatActivity {
    private Timer autoUpdate;
    private String bal = "Start to test";
    int x = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_heatmap);
        TextView balance = (TextView) findViewById(R.id.balance);
        balance.setText(bal);
        this.map();

    }

    public void onResume() {
        super.onResume();

        autoUpdate = new Timer();
        autoUpdate.schedule(new TimerTask() {
            @Override
            public void run() {

                runOnUiThread(new Runnable() {
                    public void run() {
                        Message message = new Message();
                        message.what = 1;
                        map();


                    }
                });
            }
        }, 0, 1000); // updates each 0.5 secs
    }

    public void map() {
        ImageView heatmap1 = (ImageView) findViewById(R.id.heatmap1);
        ImageView heatmap2 = (ImageView) findViewById(R.id.heatmap2);


        Picasso.with(this).load("http://184.72.70.209:8081/img/testl.png").memoryPolicy(MemoryPolicy.NO_CACHE)
                .networkPolicy(NetworkPolicy.NO_CACHE)
                .into(heatmap1);

        Picasso.with(this).load("http://184.72.70.209:8081/img/testr.png").memoryPolicy(MemoryPolicy.NO_CACHE)
                .networkPolicy(NetworkPolicy.NO_CACHE)
                .into(heatmap2);



    }



}