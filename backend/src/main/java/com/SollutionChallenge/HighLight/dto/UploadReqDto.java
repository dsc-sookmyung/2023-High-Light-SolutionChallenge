package com.SollutionChallenge.HighLight.dto;

import lombok.*;
import org.springframework.web.multipart.MultipartFile;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class UploadReqDto {
    private String user_name;
    private Long user_id;
    private MultipartFile uploaded_file;
}