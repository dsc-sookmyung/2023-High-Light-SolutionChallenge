package com.SollutionChallenge.HighLight.Folder;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FolderResponseDto {
	private Long id;
	private String folderName;

	public FolderResponseDto(Long id, String folderName) {
		this.id = id;
		this.folderName = folderName;
	}

	public static FolderResponseDto from(Long id, String folderName){
		FolderResponseDto folderResponseDto  = new FolderResponseDto(id, folderName);
		folderResponseDto.id = id;
		folderResponseDto.folderName = folderName;
		return folderResponseDto;
	}


}

