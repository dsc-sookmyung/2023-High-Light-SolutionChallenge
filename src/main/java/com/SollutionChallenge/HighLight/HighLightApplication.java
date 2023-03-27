package com.SollutionChallenge.HighLight;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

// @EnableJpaAuditing
@SpringBootApplication
@ComponentScan(basePackages = {"com.SollutionChallenge.HighLight","com.SollutionChallenge.HighLight.User"})
public class HighLightApplication {
	public static void main(String[] args) {
		SpringApplication.run(HighLightApplication.class, args);

	}

}
