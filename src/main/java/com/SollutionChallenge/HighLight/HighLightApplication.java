package com.SollutionChallenge.HighLight;

import com.SollutionChallenge.HighLight.controller.GCSController;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;


@EnableAutoConfiguration(exclude = {DataSourceAutoConfiguration.class})
@ComponentScan(basePackages = "com.SollutionChallenge.HighLight")
public class HighLightApplication {

	public static void main(String[] args) {
		SpringApplication.run(HighLightApplication.class, args);
	}

}
