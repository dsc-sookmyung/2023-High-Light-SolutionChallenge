package com.SollutionChallenge.HighLight.File;

import lombok.*;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class GetPageResDto {
    private Long page_id;
    private FullTextInfoDto full_text;
    private List<TextInfoDto> text;
    private List<ImageInfoDto> image;
}
