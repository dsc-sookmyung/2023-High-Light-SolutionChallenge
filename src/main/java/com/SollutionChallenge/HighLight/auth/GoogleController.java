package com.SollutionChallenge.HighLight.auth;

import com.SollutionChallenge.HighLight.common.ApiResponse;
import com.SollutionChallenge.HighLight.common.Success;
import com.SollutionChallenge.HighLight.dto.TokenDto;
import com.SollutionChallenge.HighLight.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;


import java.io.IOException;


@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/google")
public class GoogleController {
	@Autowired
	AuthService authService;

	@PostMapping(value = "/login")
	public ApiResponse googleLogin(@RequestBody GoogleLoginResponse googleLoginResponse) throws IOException {
		String accessToken = googleLoginResponse.getAccess_token();
		String idToken = googleLoginResponse.getId_token();
		System.out.println(accessToken);

		return ApiResponse.successCode(Success.CREATE_USER_SUCCESS, authService.googleLogin(accessToken));
	}
	/* ResponseEntity 사용해서 헤더에 status code 담는 버전 */
//	@PostMapping(value = "/login")
//	public ResponseEntity<TokenDto> googleLogin(@RequestBody GoogleLoginResponse googleLoginResponse) throws IOException {
//		HttpHeaders headers = new HttpHeaders();
//		headers.set("Status-Code", String.valueOf(HttpStatus.OK));
//
//		String accessToken = googleLoginResponse.getAccess_token();
//		String idToken = googleLoginResponse.getId_token();
//		System.out.println(accessToken);
//
//		return ResponseEntity
//				.status(HttpStatus.OK)
//				.headers(headers)
//				.body(authService.googleLogin(accessToken));
//	}
}