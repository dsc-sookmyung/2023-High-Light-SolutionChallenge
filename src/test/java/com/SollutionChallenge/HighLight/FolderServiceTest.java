package com.SollutionChallenge.HighLight;

import java.lang.reflect.Member;
import java.util.List;

import org.junit.jupiter.api.Test;

import com.SollutionChallenge.HighLight.Folder.Folder;
import com.SollutionChallenge.HighLight.Folder.FolderRepository;
import static org.assertj.core.api.Assertions.assertThat;


public class FolderServiceTest {
	FolderRepository folderRepository;
	Folder folder;

	@Test
	void findAll() {
		folderRepository.save(folder);
		List<Folder> list = folderRepository.findAll();
		assertThat(list.size()).isEqualTo(0);
	}

}
