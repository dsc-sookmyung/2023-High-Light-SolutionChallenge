package com.SollutionChallenge.HighLight.Folder;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
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
	private ApiResponse<Map<String, List<FolderResponseDto>>> getFolder(){
		Map<String, List<FolderResponseDto>> response = folderService.viewFolder();
		return ApiResponse.successCode(Success.GET_FOLDER_SUCCESS,response);
	}

	@GetMapping("/folder/{folder_id}")
	private ApiResponse getOneFolder(@PathVariable Long folder_id){
		FolderResponseDto response = folderService.viewOneFolder(folder_id);
		return ApiResponse.successCode(Success.GET_FOLDER_SUCCESS,response);
	}
}
