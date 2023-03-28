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
	private User user;

	@Column(nullable = false)
	private String fileName;

	@Column(nullable = false)
	private String fileUrl;

	@Column(nullable = false)
	private boolean converted = false; //반환 여부 저장

	public static File createFile(Long id, User user, String fileName, String fileUrl) {
		File file= new File();
		file.user = user;
		file.fileName = fileName;
		file.fileUrl = fileUrl;
		return file;
	}
	// 변환 여부 확인 메소드
	public boolean isConverted() {
		return converted;
	}

	// 변환 여부 설정 메소드
	public void setConverted(boolean converted) {
		this.converted = converted;
	}

}
