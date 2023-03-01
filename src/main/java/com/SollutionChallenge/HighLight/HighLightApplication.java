package com.SollutionChallenge.HighLight;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;


@EnableAutoConfiguration(exclude = {DataSourceAutoConfiguration.class})
public class HighLightApplication {

	public static void main(String[] args) {
		SpringApplication.run(HighLightApplication.class, args);
	}

}
