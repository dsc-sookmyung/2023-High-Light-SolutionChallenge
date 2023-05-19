package com.SollutionChallenge.HighLight.service;

import com.SollutionChallenge.HighLight.User.Entity.Role;
import com.SollutionChallenge.HighLight.User.Entity.User;
import com.SollutionChallenge.HighLight.User.UserRepository;
import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;
import com.SollutionChallenge.HighLight.dto.GoogleUserInfoDto;
import com.SollutionChallenge.HighLight.dto.TokenDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

@Service
@RequiredArgsConstructor
public class AuthService {
    @Autowired
    private final JwtTokenUtil jwtTokenUtil;

    private final UserRepository userRepository;

    @Transactional
    public TokenDto googleLogin(String accessToken) throws IOException {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        User user = null;
        headers.add("Authorization", "Bearer " + accessToken);
        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(headers);
        ResponseEntity<String> response = restTemplate.exchange("https://www.googleapis.com/oauth2/v1/userinfo", HttpMethod.GET, request,String.class);
        System.out.println("response.getBody() = " + response.getBody());

        ObjectMapper objectMapper = new ObjectMapper();
        GoogleUserInfoDto googleUser = objectMapper.readValue(response.getBody(), GoogleUserInfoDto.class);

        if (userRepository.findByEmail(googleUser.getEmail()).orElse(null) == null) {
            System.out.println("------------userRepository에 없음, 새로 만들기: "+googleUser.getEmail());
            user = User.builder()
                    .name(googleUser.getName())
                    .email(googleUser.getEmail())
                    .picture(googleUser.getPicture())
                    .role(Role.USER)
                    .build();

            userRepository.save(user);
        }
        user = userRepository.findByEmail(googleUser.getEmail()).get();
        String jwt = jwtTokenUtil.generateToken(user);
        System.out.println("googleUser email: "+googleUser.getEmail());
        System.out.println("token: "+jwt+", googleUserName: "+googleUser.getName());

        User currentUser = userRepository.findByEmail(googleUser.getEmail()).get();

        TokenDto tokenDto = TokenDto.builder()
                .token(jwt)
                .user_id(currentUser.getId())
                .build();

        return tokenDto;

    }
}
