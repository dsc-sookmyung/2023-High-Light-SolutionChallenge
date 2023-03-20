package com.SollutionChallenge.HighLight.auth;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class GoogleLoginResponse {
	private String access_token; // 애플리케이션이 Google API 요청을 승인하기 위해 보내는 토큰
	private String id_token;
}