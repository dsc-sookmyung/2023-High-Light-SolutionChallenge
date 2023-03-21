package com.SollutionChallenge.HighLight.common;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class ApiResponse<T> {
	private ApiHeader header;
	private ApiBody body;
	private static int SUCCESS = 200;


	private ApiResponse(ApiHeader header, ApiBody body){
		this.header = header;
		this.body = body;
	}

	public ApiResponse(ApiHeader header){
		this.header = header;
	}

	public static <T> ApiResponse<T> successCode(Success success, T data) {
		return new ApiResponse<T>(new ApiHeader(success.getStatus(), success.getMessage()), new ApiBody(data, success.getMessage()));
	}

}