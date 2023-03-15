package com.SollutionChallenge.HighLight.Folder;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class FolderService {
	FolderRepository folderRepository;
	// @Transactional
	// public Folder getFolder() {
	// 	return folderRepository.findAll();
	// }
}
