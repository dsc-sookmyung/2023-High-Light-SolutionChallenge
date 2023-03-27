package com.SollutionChallenge.HighLight;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;


@SpringBootApplication
@ComponentScan(basePackages = {"com.SollutionChallenge.HighLight","com.SollutionChallenge.HighLight.User"})
public class HighLightApplication {

	public static void main(String[] args) {
		SpringApplication.run(HighLightApplication.class, args);
	}

}
