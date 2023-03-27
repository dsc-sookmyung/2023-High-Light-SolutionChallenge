package com.SollutionChallenge.HighLight.File;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.SollutionChallenge.HighLight.Folder.Folder;
import com.SollutionChallenge.HighLight.Folder.FolderRepository;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class FileService {
	private final FileRepository fileRepository;
	private final File file;

	@Autowired
	public FileService(FileRepository fileRepository) {
		this.fileRepository = fileRepository;
		this.file = File.createFile(null, null, null);
	}

}
