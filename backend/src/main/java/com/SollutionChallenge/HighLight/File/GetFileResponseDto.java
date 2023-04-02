package com.SollutionChallenge.HighLight.File;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class GetFileResponseDto {
    private Long file_id;
    private int page_count;
}
