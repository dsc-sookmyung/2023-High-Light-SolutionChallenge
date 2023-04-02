package com.SollutionChallenge.HighLight.File;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class SendTextInfoDto {
    private String audio_url;
    private int font_size;
    private String text_content;
}
