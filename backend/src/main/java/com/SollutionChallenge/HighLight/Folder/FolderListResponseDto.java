package com.SollutionChallenge.HighLight.Folder;

import java.util.List;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class FolderListResponseDto {
	private List<FolderResponseDto> folderList;

	public FolderListResponseDto(List<FolderResponseDto> folderList) {
		this.folderList = folderList;
	}
}
