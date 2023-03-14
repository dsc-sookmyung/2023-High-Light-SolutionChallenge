package com.SollutionChallenge.HighLight.User;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class UserController {
	@Autowired
	private UserRepository userRepository;
	@Autowired private BCryptPasswordEncoder bCryptPasswordEncoder;

	//new
	@GetMapping("/login")
	public String loginPage(){
		return "login";
	}

	// @GetMapping("/oauth2/redirect")
	// public String oauth2Redirect(@AuthenticationPrincipal OAuth2User principal){
	// 	String email = principal.getAttribute("email");
	// 	String name = principal.getAttribute("name");
	// }

}
