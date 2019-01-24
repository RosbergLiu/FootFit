package com.example.jiyuan.a;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class Pressure extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pressure);
        TextView left_ratio = findViewById(R.id.left_ratio);
        TextView right_ratio = findViewById(R.id.right_ratio);
        Intent intent = getIntent();
        Bundle bundle = new Bundle();
        bundle = intent.getExtras();
        String left = bundle.getString("left_ratio");
        String right = bundle.getString("right_ratio");
        left_ratio.setText("left_ratio:" + '\n' + left + "%");
        right_ratio.setText("right_ratio:" + '\n' + right + "%");

    }
}
