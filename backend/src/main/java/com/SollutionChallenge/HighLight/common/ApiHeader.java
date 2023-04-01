package com.SollutionChallenge.HighLight.common;

import org.springframework.http.HttpStatus;

public class ApiHeader {
	private HttpStatus status;
	private String message;

	public ApiHeader(HttpStatus status, String message) {
		this.status = status;
		this.message = message;
	}

	public HttpStatus getStatus() {
		return status;
	}

	public String getMessage() {
		return message;
	}
}
