package com.SollutionChallenge.HighLight.Conversion;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import com.SollutionChallenge.HighLight.File.File;
import com.SollutionChallenge.HighLight.File.FileRepository;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class FileConversionController {

	@Autowired
	private FileRepository fileRepository;

	@GetMapping("/conversion/status/{fileId}")
	public ResponseEntity<Boolean> getConversionStatus(@PathVariable Long fileId) {
		Optional<File> optionalFile = fileRepository.findById(fileId);

		if (optionalFile.isPresent()) {
			File file = optionalFile.get();
			return ResponseEntity.ok(file.isConverted());
		} else {
			return ResponseEntity.notFound().build();
		}
	}
}
