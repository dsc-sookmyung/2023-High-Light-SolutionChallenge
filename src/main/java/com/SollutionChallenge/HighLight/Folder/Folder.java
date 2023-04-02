package com.SollutionChallenge.HighLight.Folder;

import javax.persistence.*;


import com.SollutionChallenge.HighLight.File.File;
import com.SollutionChallenge.HighLight.User.Entity.User;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

@Entity
@Table(name = "Folder")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Folder {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "folder_id",nullable = false, unique = true)
	private Long id;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "user_id")
	private User userId;

	@OneToMany(mappedBy = "folder", cascade = CascadeType.ALL)
	private List<File> fileList;

	@Column(nullable = false)
	private String name;


	public static Folder createFolder( User userId, String name){
		Folder folder = new Folder();
		// folder.id = id;
		folder.userId=userId;
		folder.name=name;

		return folder;

	}

}
