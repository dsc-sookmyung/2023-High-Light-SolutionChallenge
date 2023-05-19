package com.SollutionChallenge.HighLight.Folder;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FileResponseDto {
    private Long file_id;
    private String file_name;
    private String file_img;

    public FileResponseDto(Long file_id,String file_name,String file_img) {
        this.file_id = file_id;
        this.file_name = file_name;
        this.file_img = file_img;
    }


}