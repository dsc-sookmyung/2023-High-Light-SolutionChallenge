package com.SollutionChallenge.HighLight.Folder;

import java.util.List;
import java.util.Optional;

import com.SollutionChallenge.HighLight.User.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import com.sun.istack.NotNull;

@Repository
public interface FolderRepository extends JpaRepository<Folder, Long> {
	// List<Folder> findAll();
    List<Folder> findAllByUserId(User user);
    Optional<Folder> findByIdAndUserId(Long folder_id, User user);
}
