package com.SollutionChallenge.HighLight.File;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ImageInfoDto {
    private Long img_idx;
    private String img_url;
    private String img_text;
    private String img_audio_url;
}
