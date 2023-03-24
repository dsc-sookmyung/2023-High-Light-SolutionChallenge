package com.SollutionChallenge.HighLight.auth;

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

	/* ResponseEntity 사용해서 헤더에 status code 담는 버전 */
	@PostMapping(value = "/login")
	public ResponseEntity<TokenDto> googleLogin(@RequestBody GoogleLoginResponse googleLoginResponse) throws IOException {
		String accessToken = googleLoginResponse.getAccess_token();
		String idToken = googleLoginResponse.getId_token();
		System.out.println("========== user's accessToken: " + accessToken + " ==========");

		return ResponseEntity
				.status(HttpStatus.OK)
				.body(authService.googleLogin(accessToken));
	}

}