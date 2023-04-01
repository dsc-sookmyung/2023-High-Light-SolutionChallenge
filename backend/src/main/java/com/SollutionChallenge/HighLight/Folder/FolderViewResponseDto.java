package com.SollutionChallenge.HighLight.Folder;

import java.util.List;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FolderViewResponseDto {
	private List<Long> id;
	private List<String> folderName;

	public static FolderViewResponseDto of(List <Long> id,List<String >folderName){
		FolderViewResponseDto folderViewResponseDto = new FolderViewResponseDto();
		folderViewResponseDto.id= id;
		folderViewResponseDto.folderName = folderName;

		return folderViewResponseDto;
	}
}
