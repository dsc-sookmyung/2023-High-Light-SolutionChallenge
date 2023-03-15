package com.SollutionChallenge.HighLight.User.Entity;

import java.security.Timestamp;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.annotations.CreationTimestamp;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@NoArgsConstructor
@Entity
public class User  {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Column(nullable = false)
	private String name;

	@Column(nullable = false)
	private String email;

	@Column
	private String picture;

	/*
	@Enumerated(EnumType.STRING)
	JPA로 데이터베이스로 저장할 때 Enum 값을 어떤 형태로 저장할지를 결정함
	기본적으로는 int로 된 숫자가 저장된다.
	숫자로 저장되면 데이터베이스로 확인할 때 그 값이 무슨 코드를 의미하는지 알 수 가 없다.
	그래서 문자열로 저장될 수 있도록 선언
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private Role role;

	@Builder
	public User(String name, String email, String picture, Role role){
		this.name = name;
		this.email = email;
		this.picture = picture;
		this.role = role;
	}

	public User update(String name, String picture){
		this.name = name;
		this.picture = picture;

		return this;
	}

	public String getRoleKey(){
		return this.role.getKey();
	}

}