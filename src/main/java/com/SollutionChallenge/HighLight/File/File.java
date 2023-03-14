package com.SollutionChallenge.HighLight.File;

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
@Table(name = "file")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class File {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "file_id", unique = true, nullable = false)
	@Getter
	private Long id;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "user_id", nullable = false)
	private User userId;

	@Column(nullable = false)
	private String fileName;

	@Column(nullable = false)
	private String fileUrl;

	private static File createFile(Long id, User userId, String fileName, String fileUrl) {
		File file= new File();
		file.id=id;
		file.userId=userId;
		file.fileName=fileName;
		file.fileUrl=fileUrl;
		return new File();
	}

}
