package com.SollutionChallenge.HighLight.auth;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.stereotype.Component;

import com.google.api.client.util.Value;

@Component
public class ConfigUtils {
	@Value("${google.auth.url}")
	private String googleAuthUrl;

	@Value("${google.login.url}")
	private String googleLoginUrl;

	@Value("${google.redirect.uri}")
	private String googleRedirectUrl;

	@Value("${google.client.id}")
	private String googleClientId;

	@Value("${google.secret}")
	private String googleSecret;

	@Value("${google.auth.scope}")
	private String scopes;

	// Google 로그인 URL 생성 로직
	public String googleInitUrl() {
		Map<String, Object> params = new HashMap<>();
		params.put("client_id", getGoogleClientId());
		params.put("redirect_uri", getGoogleRedirectUri());
		params.put("response_type", "code");
		params.put("scope", getScopeUrl());

		String paramStr = params.entrySet().stream()
			.map(param -> param.getKey() + "=" + param.getValue())
			.collect(Collectors.joining("&"));

		return getGoogleLoginUrl()
			+ "/o/oauth2/v2/auth"
			+ "?"
			+ paramStr;
	}

	public String getGoogleAuthUrl() {
		return googleAuthUrl;
	}

	public String getGoogleLoginUrl() {
		return googleLoginUrl;
	}

	public String getGoogleClientId() {
		return googleClientId;
	}

	public String getGoogleRedirectUri() {
		return googleRedirectUrl;
	}

	public String getGoogleSecret() {
		return googleSecret;
	}

	// scope의 값을 보내기 위해 띄어쓰기 값을 UTF-8로 변환하는 로직 포함
	public String getScopeUrl() {
		//        return scopes.stream().collect(Collectors.joining(","))
		//                .replaceAll(",", "%20");
		return scopes.replaceAll(",", "%20");
	}
	// public User toEntity(GoogleLoginRequest oauth2UserInfo) {
	// 	return User.builder()
	// 		.socialId(oauth2UserInfo.getId())
	// 		.build();
	// }
}
