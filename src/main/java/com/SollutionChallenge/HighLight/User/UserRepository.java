package com.SollutionChallenge.HighLight.User;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.SollutionChallenge.HighLight.User.Entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
	Optional<User> findByEmail(String email);

	User findByUsername(String username);
}
