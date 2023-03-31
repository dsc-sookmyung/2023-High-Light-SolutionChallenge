package com.SollutionChallenge.HighLight.Folder;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.SollutionChallenge.HighLight.File.FileService;
import com.SollutionChallenge.HighLight.User.Entity.User;
import com.SollutionChallenge.HighLight.User.UserRepository;
import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class FolderController {
	private final FolderService folderService;
	private final JwtTokenUtil jwtTokenUtil;
	private final UserRepository userRepository;
	private final FileService fileService;
	@PostMapping("/folder")
	public ResponseEntity<Map<String, Map<String, List<FolderResponseDto>>>> createFolder(
			@RequestHeader("token") String jwtToken, @RequestBody FolderRequestDto folderRequestDto) {
		Long userId = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
		Map<String, List<FolderResponseDto>> folderMap = folderService.save(userId, folderRequestDto);
		Map<String, Map<String, List<FolderResponseDto>>> response = new HashMap<>();
		Map<String, List<FolderResponseDto>> dataMap = new HashMap<>();
		dataMap.put("folder", folderMap.get("folder"));
		response.put("data", dataMap);
		return ResponseEntity.ok(response);
	}

	@GetMapping("/folder")
	public ResponseEntity<Map<String, Map<String, List<FolderResponseDto>>>> getFolder(@RequestHeader("token") String jwtToken) {
		System.out.println("jwtToken: " + jwtToken);
		Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
		User currentUser = userRepository.findById(user_id).get();
		Map<String, List<FolderResponseDto>> folderMap = folderService.viewFolder(currentUser);
		Map<String, Map<String, List<FolderResponseDto>>> response = new HashMap<>();
		Map<String, List<FolderResponseDto>> dataMap = new HashMap<>();
		dataMap.put("folder", folderMap.get("folder"));
		response.put("data", dataMap);
		return ResponseEntity.ok(response);
	}



	@GetMapping("/folder/{folderId}")
	public ResponseEntity<Map<String, Map<String, List<FileResponseDto>>>> getFilesInFolder(
			@RequestHeader("token") String jwtToken, @PathVariable Long folderId) {
		System.out.println("jwtToken: " + jwtToken);
		Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
		User currentUser = userRepository.findById(user_id).get();
		Map<String, List<FileResponseDto>> fileMap = fileService.viewFolderFile(user_id);
		Map<String, Map<String, List<FileResponseDto>>> response = new HashMap<>();
		Map<String, List<FileResponseDto>> dataMap = new HashMap<>();
		dataMap.put("files", fileMap.get("file"));
		response.put("data", dataMap);
		return ResponseEntity.ok(response);
	}

}