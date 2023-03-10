package com.SollutionChallenge.HighLight.dto;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
public class TokenDto {
    private String token;
    private String name;
    private String email;
    private String profile_pic;
}