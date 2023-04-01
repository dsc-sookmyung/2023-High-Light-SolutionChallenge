package com.SollutionChallenge.HighLight.common;

import static org.springframework.http.HttpStatus.*;
import org.springframework.http.HttpStatus;
import com.google.api.Http;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Success {

	CREATE_FOLDER_SUCCESS(OK,"폴더 생성 성공"),
	GET_FOLDER_SUCCESS(OK,"폴더 조회 성공"),
	DELETE_FOLDER_SUCCESS(OK,"폴더 삭제 성공"),
  	CREATE_USER_SUCCESS(OK, "유저 생성 성공");

	private final HttpStatus status;
	private final String message;

	// Success(HttpStatus status, String message){
	// 	this.status = status;
	// 	this.message=message;
	// }
	// public HttpStatus getStatus(){
	// 	return status;
	// }
	//
	// public String getMessage(){
	// 	return message;
	// }
}
