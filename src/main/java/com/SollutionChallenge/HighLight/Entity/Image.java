package com.SollutionChallenge.HighLight.Entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

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
		return new Image(id, fileId, pageId, imageDescription, imageUrl, voiceUrl);
	}
}
