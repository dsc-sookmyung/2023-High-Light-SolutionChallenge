package com.SollutionChallenge.HighLight.Folder;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.SollutionChallenge.HighLight.common.ApiResponse;
import com.SollutionChallenge.HighLight.common.Success;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class FolderController {
	private final FolderService folderService;

	@PostMapping("/folder")
	private ApiResponse createFolder(@RequestBody FolderRequestDto folderRequestDto){
		FolderResponseDto response = folderService.save(folderRequestDto);
		return ApiResponse.successCode(Success.CREATE_FOLDER_SUCCESS,response);
	}

	@GetMapping("/folder")
	private ApiResponse <FolderViewResponseDto>getFolder(){
		FolderViewResponseDto response = folderService.viewFolder();
		return ApiResponse.successCode(Success.GET_FOLDER_SUCCESS,response);
	}

	// @GetMapping("/folder")
	// private Folder getFolder(){
	// 	return folderService.getFolder();
	// }
}
