package com.SollutionChallenge.HighLight.dto;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class GoogleUserInfoDto {
    private String id;
    private String email;
    private Boolean verified_email;
    private String name;
    private String given_name;
    private String family_name;
    private String picture;
    private String locale;

    private String hd;
    public GoogleUserInfoDto(String id, String email, boolean verified_email, String name, String given_name, String family_name, String picture, String locale) {}
    public GoogleUserInfoDto(String id, String email, boolean verified_email, String name, String given_name, String family_name, String picture, String locale, String hd) {}
}
