package com.SollutionChallenge.HighLight.Folder;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.SollutionChallenge.HighLight.User.User;
import com.SollutionChallenge.HighLight.User.UserRepository;
import com.SollutionChallenge.HighLight.auth.ConfigUtils;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class FolderService {

	private final FolderRepository folderRepository;
	// private final
	private final Folder folder;
	// private final UserRepository userRepository;

	@Autowired
	public FolderService(FolderRepository folderRepository) {
		this.folderRepository = folderRepository;
		this.folder = Folder.createFolder(null, null);
	}

	// @Transactional
	// public FolderResponseDto save(FolderRequestDto folderRequestDto) {
	// 	String folderName = folderRequestDto.getFolderName();
	// 	return FolderResponseDto.from( folderName);
	// }

	// public FolderViewResponseDto viewFolder() {
	// 	String id = folder.getName();
	// 	List<Folder> folderName= folderRepository.findAll();
	// 	return FolderViewResponseDto.of(folderName);
	// }

	@Transactional
	public FolderResponseDto save(FolderRequestDto folderRequestDto) {
		User userId = folder.getUserId(); // 해당 폴더를 생성한 유저 정보
		String folderName = folderRequestDto.getFolderName();
		Folder savedFolder = folderRepository.save(Folder.createFolder(userId, folderName));
		return FolderResponseDto.from(savedFolder.getId(), savedFolder.getName());
	}


	public FolderViewResponseDto viewFolder() {
		List<Folder> folders = folderRepository.findAll();
		List<String> folderNames = Collections.emptyList();
		if (folders != null && !folders.isEmpty()) {
			folderNames = folders.stream()
				.filter(f -> f.getName() != null)
				.map(Folder::getName)
				.collect(Collectors.toList());
		}
		return FolderViewResponseDto.of(folderNames);
	}

	public FolderResponseDto viewOneFolder(Long folder_id) {
		Optional<Folder> folder = folderRepository.findById(folder_id);
		if(folder.isPresent()){
			String folderName = folder.get().getName();
		}
		return FolderResponseDto.from(folder_id,folder.get().getName());

	}
}
