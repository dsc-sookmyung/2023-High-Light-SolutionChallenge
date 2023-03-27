package com.SollutionChallenge.HighLight.File;

import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class FileController {
	private final FileService fileService;


}
