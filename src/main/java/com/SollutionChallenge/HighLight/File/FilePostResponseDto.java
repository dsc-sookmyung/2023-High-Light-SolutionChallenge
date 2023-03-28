package com.SollutionChallenge.HighLight.File;


import lombok.*;

@Getter
@Setter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FilePostResponseDto {
    private Long file_id;
    private int expected_sec;

    @Builder
    public FilePostResponseDto(Long file_id, int expected_sec) {
        this.file_id = file_id;
        this.expected_sec = expected_sec;
    }
}
