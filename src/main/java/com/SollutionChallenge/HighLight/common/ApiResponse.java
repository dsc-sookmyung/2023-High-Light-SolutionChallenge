package com.SollutionChallenge.HighLight.common;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class ApiResponse<T> {
	private int status;
	private T data;
	private String message;

	private ApiResponse(int status, String message, T data) {
		this.status = status;
		this.data = data;
		this.message = message;
	}

	public static <T> ApiResponse<T> successCode(Success success, T data){
		return new ApiResponse<>(success.getStatus().value(), success.getMessage(),null);
	}

}
