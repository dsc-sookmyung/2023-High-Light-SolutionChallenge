package com.SollutionChallenge.HighLight.Image;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.SollutionChallenge.HighLight.File.File;
import com.SollutionChallenge.HighLight.Page.Page;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "image")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Image {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "image_id", unique = true, nullable = false)
	@Getter
	private Long id;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "file_id", nullable = false)
	private File fileId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "page_id", nullable = false)
	private Page pageId;

	@Column(nullable = false)
	private String imageDescription;

	@Column(nullable = false)
	private String imageUrl;

	@Column(nullable = false)
	private String voiceUrl;

	private static Image createImage(Long id, File fileId, Page pageId, String imageDescription, String imageUrl,
		String voiceUrl) {
		Image image = new Image();
		image.id = id;
		image.fileId = fileId;
		image.pageId = pageId;
		image.imageDescription = imageDescription;
		image.imageUrl = imageUrl;
		image.voiceUrl = voiceUrl;
		return new Image();
	}
}
