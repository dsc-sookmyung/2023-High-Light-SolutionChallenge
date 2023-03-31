package com.SollutionChallenge.HighLight.File;

import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;

@RestController
@RequiredArgsConstructor
public class FileController {
    private final FileService fileService;
    private final JwtTokenUtil jwtTokenUtil;

    @PostMapping(value = "/folder/{folder_id}/files", consumes = MediaType.MULTIPART_FORM_DATA_VALUE/*, produces = "application/json"*/)
    public ResponseEntity<HashMap<String, FilePostResponseDto>> addFile(@RequestHeader("token") String jwtToken, @RequestHeader("Content-Type") String contentType, @RequestPart String file_name, @RequestPart MultipartFile file,/*@ModelAttribute FileRequestDto fileRequestDto,*/ @PathVariable Long folder_id) throws IOException {
        System.out.println("jwtToken: " + jwtToken);
        Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
        HashMap<String, FilePostResponseDto> map = new HashMap<>();

        System.out.println("header contentType: "+contentType);
        System.out.println("real content type: "+file.getContentType());
        FileRequestDto fileRequestDto = new FileRequestDto(file, file_name);
        map.put("data", fileService.addFile(user_id, folder_id, fileRequestDto));
//        System.out.println("real content type: "+fileRequestDto.getFile().getContentType());
//        map.put("data", fileService.addFile(user_id, folder_id, fileRequestDto));
        return ResponseEntity.ok(map);
    }


    // 특정 파일 조회
    @GetMapping("/files/{file_id}")
    public ResponseEntity<HashMap<String, GetFileResponseDto>> getFile(@RequestHeader("token") String jwtToken, @PathVariable Long file_id) {
        System.out.println("jwtToken: " + jwtToken);
        Long user_id = Long.valueOf(jwtTokenUtil.getUserIdFromToken(jwtToken));
        HashMap<String, GetFileResponseDto> map = new HashMap<>();
        map.put("data", fileService.getFile(user_id, file_id));
        return ResponseEntity.ok(map);
    }
}