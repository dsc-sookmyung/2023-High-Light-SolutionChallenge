package com.SollutionChallenge.HighLight.Folder;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import com.sun.istack.NotNull;

@Repository
public interface FolderRepository extends JpaRepository<Folder, Long> {
	// List<Folder> findAll();

}
