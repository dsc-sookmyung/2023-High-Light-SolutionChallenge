package com.SollutionChallenge.HighLight.Folder;

import java.util.List;

import com.SollutionChallenge.HighLight.User.User;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FolderResponseDto {
	private Long id;
	private String folderName;

	public static FolderResponseDto from(Long id, String folderName){
		FolderResponseDto folderResponseDto  = new FolderResponseDto();
		folderResponseDto.id = id;
		folderResponseDto.folderName = folderName;
		return folderResponseDto;
	}
}

