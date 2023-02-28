package controller;

import dto.TokenDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import service.AuthService;

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