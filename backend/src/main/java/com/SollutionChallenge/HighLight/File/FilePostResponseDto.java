package com.SollutionChallenge.HighLight.File;


import lombok.*;

@Getter
@Setter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FilePostResponseDto {
    private Long file_id;


    @Builder
    public FilePostResponseDto(Long file_id) {
        this.file_id = file_id;
    }
}
