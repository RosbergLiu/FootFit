package com.example.jiyuan.a;

import android.content.Intent;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class results extends AppCompatActivity {
    private String url;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_results);
        TextView forefoot = findViewById(R.id.forefoot);
        TextView heel = findViewById(R.id.heel);
        TextView normalstanding = findViewById(R.id.normalstanding);
        TextView under_pron = findViewById(R.id.under_pron);
        TextView over_pron = findViewById(R.id.over_pron);
        TextView time_analysis = findViewById(R.id.time_analysis);
        Intent intent = getIntent();
        Bundle bundle = new Bundle();
        bundle = intent.getExtras();
        String l_forefoot = bundle.getString("l_forefoot");
        String l_heel = bundle.getString("l_heel");
        String l_normalstanding = bundle.getString("l_normalstanding");
        String l_under_pron = bundle.getString("l_under_pron");
        String l_over_pron = bundle.getString("l_over_pron");
        String r_forefoot = bundle.getString("r_forefoot");
        String r_normalstanding = bundle.getString("r_normalstanding");
        String r_heel = bundle.getString("r_heel");
        String r_under_pron = bundle.getString("r_under_pron");
        String r_over_pron = bundle.getString("r_over_pron");
        String timeanalysis = bundle.getString("timeanalysis");
        url = bundle.getString("url");

        forefoot.setText("l_forefoot:" + l_forefoot + "%" + '\n' + "r_forefoot" + r_forefoot + "%");
        heel.setText("l_heel:" + l_heel + "%" + "\n" + "r_heel" + r_heel + "%");
        normalstanding.setText("l_normal:" + l_normalstanding + "%" +"\n" + "r_normal" + r_normalstanding + "%");
        under_pron.setText("l_under_pron:" + l_under_pron + "%" + "\n" + "r_under_pron" + r_under_pron + "%");
        over_pron.setText("l_over_pron:" + l_over_pron + "%" + "\n" + "r_over_pron" + r_over_pron + "%");
        time_analysis.setText("time analysis:" + '\n' + timeanalysis);








    }

    public void click(View view){
        Intent intent =new Intent(Intent.ACTION_VIEW);

        Uri uri = Uri.parse(url);

        intent.setData(uri);

        startActivity(intent);
    }
}
