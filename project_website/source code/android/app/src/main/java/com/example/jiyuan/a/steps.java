package com.example.jiyuan.a;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class steps extends AppCompatActivity {
    public static final String EXTRA_MESSAGE = "test_MESSAGE";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_steps);
    }



    public void start(final View view) {

        OkHttpClient mOkHttpClient = new OkHttpClient();
        final Request request = new Request.Builder()
                .url("http://184.72.70.209:5000/start_count")
                .build();
        Call call = mOkHttpClient.newCall(request);
        call.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {

            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String htmlStr = response.body().string();
                go_test(htmlStr);

            }



        });

    }

    public void go_test(String str){
        Intent intent = new Intent(this, testing.class);
        intent.putExtra(EXTRA_MESSAGE, str);
        startActivity(intent);
    }
}
