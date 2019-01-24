package com.example.jiyuan.a;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void show_Heatmap(View view){
        Intent intent = new Intent(this, Heatmap.class);
        startActivity(intent);
    }

    public void show_steps(View view){
        Intent intent = new Intent(this, steps.class);
        startActivity(intent);
    }

    public void show_pressure(final View view) {

        OkHttpClient mOkHttpClient = new OkHttpClient();
        final Request request = new Request.Builder()
                .url("http://184.72.70.209:5000/show_bias")
                .build();
        Call call = mOkHttpClient.newCall(request);
        call.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {

            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                try {
                    JSONObject json = new JSONObject(response.body().string());
                    String left_ratio  = json.getString("left_ratio");
                    String right_ratio = json.getString("right_ratio");




                    Bundle bundle=new Bundle();
                    bundle.putString("left_ratio",left_ratio);
                    bundle.putString("right_ratio",right_ratio);
                    go_result(bundle);


                } catch (JSONException e) {
                    e.printStackTrace();
                }



            }



        });

    }



    public void go_result(Bundle bundle){
        Intent intent = new Intent(this, Pressure.class);
        intent.putExtras(bundle);
        startActivity(intent);
    }
}

