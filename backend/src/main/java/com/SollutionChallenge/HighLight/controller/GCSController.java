package com.SollutionChallenge.HighLight.controller;

import com.google.cloud.storage.Storage;
import com.SollutionChallenge.HighLight.dto.UploadReqDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.SollutionChallenge.HighLight.service.GCSService;

import java.io.IOException;

@RestController
@RequiredArgsConstructor
public class GCSController {
    @Autowired
    private GCSService gcsService;
    @Autowired
    private Storage storage;

    //@PostMapping("/upload")
    public String uploadNewFile(UploadReqDto dto, String filename, Long folderId) throws IOException {
        return gcsService.uploadNewFile(dto, filename, folderId);
    }

}
