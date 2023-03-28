package com.SollutionChallenge.HighLight.File;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.File;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class FileRequestDto {
    private File file;
    private String file_name;
}
