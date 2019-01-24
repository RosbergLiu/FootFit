package com.example.jiyuan.a;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class testing extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_testing);

        // Get the Intent that started this activity and extract the string
        Intent intent = getIntent();
        String message = intent.getStringExtra(steps.EXTRA_MESSAGE);

        // Capture the layout's TextView and set the string as its text
        TextView textView = findViewById(R.id.textView);
        textView.setText(message);

    }

    public void finish(final View view) {

        OkHttpClient mOkHttpClient = new OkHttpClient();
        final Request request = new Request.Builder()
                .url("http://184.72.70.209:5000/end_count")
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
                    String l_forefoot = json.getString("l_forefoot");
                    String l_heel = json.getString("l_heel");
                    String l_normalstanding = json.getString("l_normalstanding");
                    String l_under_pron = json.getString("l_under_pron");
                    String l_over_pron = json.getString("l_over_pron");
                    String r_forefoot = json.getString("r_forefoot");
                    String r_normalstanding = json.getString("r_normalstanding");
                    String r_heel = json.getString("r_heel");
                    String r_under_pron = json.getString("r_under_pron");
                    String r_over_pron = json.getString("r_over_pron");
                    String timeanalysis = json.getString("timeanalysis");
                    String url = json.getString("url");



                    Bundle bundle=new Bundle();
                    bundle.putString("l_forefoot",l_forefoot);
                    bundle.putString("l_heel",l_heel);
                    bundle.putString("l_normalstanding",l_normalstanding);
                    bundle.putString("l_under_pron",l_under_pron);
                    bundle.putString("l_over_pron",l_over_pron);
                    bundle.putString("r_forefoot",r_forefoot);
                    bundle.putString("r_normalstanding",r_normalstanding);
                    bundle.putString("r_heel",r_heel);
                    bundle.putString("r_under_pron",r_under_pron);
                    bundle.putString("r_over_pron",r_over_pron);
                    bundle.putString("timeanalysis",timeanalysis);
                    bundle.putString("url",url);
                    go_result(bundle);


                } catch (JSONException e) {
                    e.printStackTrace();
                }



            }



        });

    }



    public void go_result(Bundle bundle){
        Intent intent = new Intent(this, results.class);
        intent.putExtras(bundle);
        startActivity(intent);
    }
}
