package com.SollutionChallenge.HighLight.Entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.annotations.ColumnDefault;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "user")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class User {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id", unique = true, nullable = false)
	@Getter
	private Long id;

	@Column(nullable = false)
	private String email;

	@Column(nullable = false)
	private String name;

	// @Column(name = "is_deleted", columnDefinition = "TINYINT", length = 1)
	// @ColumnDefault("0")
	// @Getter
	// private boolean isDeleted = false;
	//
	// public boolean softDelete() {
	// 	if (isDeleted == true)
	// 		throw new IllegalStateException(ErrorCode.ALREADY_DELETED.getMessage());
	// 	this.isDeleted = true;
	// 	return true;}

	public static User createUser(Long id, String email, String name) {
		return new User(id, email, name);
	}

}
