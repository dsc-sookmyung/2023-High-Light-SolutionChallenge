package com.SollutionChallenge.HighLight.Folder;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.SollutionChallenge.HighLight.User.Entity.User;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "folder")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Folder {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "folder_id",nullable = false, unique = true)
	private Long id;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "user_id", nullable = false)
	private User userId;

	private static Folder createFolder(Long id, User userId){
		Folder folder = new Folder();
		folder.id = id;
		folder.userId=userId;

		return new Folder();
	}

}
