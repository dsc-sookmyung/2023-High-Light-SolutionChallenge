package com.SollutionChallenge.HighLight.common;

import org.springframework.stereotype.Service;

import com.SollutionChallenge.HighLight.User.UserRepository;
import com.SollutionChallenge.HighLight.auth.ConfigUtils;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {
	UserRepository userRepository;
	ConfigUtils configUtils;

	// @Transactional
	// public User findUser(){
	// 	return userRepository.findById(SecurityUtil.getCurrentUserId())
	// }

}
