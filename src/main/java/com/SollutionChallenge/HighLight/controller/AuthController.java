package com.SollutionChallenge.HighLight.controller;

import com.SollutionChallenge.HighLight.dto.TokenDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import com.SollutionChallenge.HighLight.service.AuthService;

import java.io.IOException;

@Controller
@RequiredArgsConstructor
public class AuthController {
    AuthService authService;

    @PostMapping("/google/login")
    public TokenDto callback(@RequestParam String authCode) throws IOException {
        return authService.googleLogin(authCode);
    }

}