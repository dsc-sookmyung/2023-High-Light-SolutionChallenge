package com.SollutionChallenge.HighLight.Page;

import com.SollutionChallenge.HighLight.File.SendPageResDto;
import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;


import java.util.HashMap;

@RestController
@RequiredArgsConstructor
public class PageController {
    private final PageService pageService;
    private final JwtTokenUtil jwtTokenUtil;
    @GetMapping("/files/{file_id}/page/{page_id}")
    public ResponseEntity<HashMap<String, SendPageResDto>> getPageContents(@RequestHeader("token") String jwtToken, @PathVariable Long file_id, @PathVariable Long page_id) throws JsonProcessingException {
        System.out.println("jwtToken: " + jwtToken);
        Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
        HashMap<String, SendPageResDto> map = new HashMap<>();
        map.put("data", pageService.getPageContents(user_id, file_id, page_id));
        return ResponseEntity.ok(map);
    }
}
