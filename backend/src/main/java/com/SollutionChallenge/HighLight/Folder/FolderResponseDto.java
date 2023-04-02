package com.SollutionChallenge.HighLight.Folder;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FolderResponseDto {
	private Long folder_id;
	private String folder_name;

	public FolderResponseDto(Long folder_id, String folder_name) {
		this.folder_id = folder_id;
		this.folder_name = folder_name;
	}

	public static FolderResponseDto from(Long folder_id, String folder_name){
		FolderResponseDto folderResponseDto  = new FolderResponseDto(folder_id, folder_name);
		folderResponseDto.folder_id = folder_id;
		folderResponseDto.folder_name = folder_name;
		return folderResponseDto;
	}


}
