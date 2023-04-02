package com.SollutionChallenge.HighLight.Page;

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

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "page")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Page {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "page_id", unique = true, nullable = false)
	@Getter
	private Long id;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "file_id", nullable = false)
	private File fileId;

	private static Page createPage(Long id, File fileId) {
		Page page = new Page();
		page.id = id;
		page.fileId = fileId;
		return page;
	}
}
