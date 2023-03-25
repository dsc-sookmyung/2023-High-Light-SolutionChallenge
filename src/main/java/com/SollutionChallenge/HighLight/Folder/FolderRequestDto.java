package com.SollutionChallenge.HighLight.Folder;

import com.SollutionChallenge.HighLight.User.User;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class FolderRequestDto {

	private User userId;
	private String folderName;

}
