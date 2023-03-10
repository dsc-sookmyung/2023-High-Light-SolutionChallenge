package com.SollutionChallenge.HighLight.dto;

import lombok.*;
import org.springframework.web.multipart.MultipartFile;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class UploadReqDto {
    private String userName;
    private MultipartFile image;
}