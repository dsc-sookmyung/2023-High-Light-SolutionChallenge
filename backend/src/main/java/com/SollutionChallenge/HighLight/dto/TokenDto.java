package com.SollutionChallenge.HighLight.dto;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
public class TokenDto {
    private Long user_id;
    private String token;
}