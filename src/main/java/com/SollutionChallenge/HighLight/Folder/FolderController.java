package com.SollutionChallenge.HighLight.Folder;

import java.util.List;
import java.util.Map;

import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;
import org.springframework.web.bind.annotation.*;

import com.SollutionChallenge.HighLight.common.ApiResponse;
import com.SollutionChallenge.HighLight.common.Success;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class FolderController {
	private final FolderService folderService;
	private final JwtTokenUtil jwtTokenUtil;

	@PostMapping("/folder")
	private ApiResponse createFolder(@RequestHeader("token") String jwtToken, @RequestBody FolderRequestDto folderRequestDto){
		System.out.println("jwtToken: " + jwtToken);
		Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
		FolderResponseDto response = folderService.save(user_id, folderRequestDto);
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
