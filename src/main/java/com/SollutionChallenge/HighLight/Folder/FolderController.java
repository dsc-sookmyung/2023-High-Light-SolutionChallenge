package com.SollutionChallenge.HighLight.Folder;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.SollutionChallenge.HighLight.User.Entity.User;
import com.SollutionChallenge.HighLight.common.ApiResponse;
import com.SollutionChallenge.HighLight.common.Success;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping()
@RequiredArgsConstructor
public class FolderController {
	FolderService folderService;

	@PostMapping("/folder")
	private ApiResponse createFolder(@RequestBody User userId){
		return ApiResponse.successCode(Success.CREATE_FOLDER_SUCCESS,userId);
	}

	// @GetMapping("/folder")
	// private Folder getFolder(){
	// 	return folderService.getFolder();
	// }
}
