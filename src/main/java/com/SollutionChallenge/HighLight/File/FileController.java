package com.SollutionChallenge.HighLight.File;

import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.HashMap;

@RestController
@RequiredArgsConstructor
public class FileController {
    private final FileService fileService;
    private final JwtTokenUtil jwtTokenUtil;

    @PostMapping("/folder/{folder_id}/files")
    public ResponseEntity<HashMap<String, FilePostResponseDto>> addFile(@RequestHeader("token") String jwtToken, FileRequestDto fileRequestDto, @PathVariable Long folder_id) throws IOException {
        System.out.println("jwtToken: " + jwtToken);
        Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
        HashMap<String, FilePostResponseDto> map = new HashMap<>();
        map.put("data", fileService.addFile(user_id, folder_id, fileRequestDto));
        return ResponseEntity.ok(map);
    }

    }