package com.SollutionChallenge.HighLight.File;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class TextInfoDto {
    private String audio_url;
    private int font_size;
    private String text; // text_content
}
