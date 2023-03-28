package com.SollutionChallenge.HighLight.File;

import com.SollutionChallenge.HighLight.User.Entity.User;
import com.SollutionChallenge.HighLight.User.UserRepository;
import com.SollutionChallenge.HighLight.controller.GCSController;
import com.SollutionChallenge.HighLight.dto.UploadReqDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import java.io.FileInputStream;
import java.io.IOException;

import org.springframework.mock.web.MockMultipartFile;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.commons.CommonsMultipartFile;

import java.io.*;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@RequiredArgsConstructor
@Service
public class FileService {
    private final FileRepository fileRepository;
    private final UserRepository userRepository;
    private final GCSController gcsController;

    @Transactional
    public FilePostResponseDto addFile(Long userId, Long folderId, FileRequestDto fileRequestDto) throws IOException {
        MultipartFile multipartFile = fileRequestDto.getFile();
        String filename = fileRequestDto.getFile_name();

        // 파일 gcs에 업로드
        User currentUser = userRepository.findById(userId).get();
        UploadReqDto uploadReqDto = new UploadReqDto(currentUser.getName(), userId, multipartFile);
        String uploadedFileUrl = gcsController.uploadNewFile(uploadReqDto, folderId);

        // 후 createFile(User user, String fileName, String fileUrl)로 filerepository에 저장
        com.SollutionChallenge.HighLight.File.File newFile = com.SollutionChallenge.HighLight.File.File.createFile(currentUser, multipartFile.getOriginalFilename(),uploadedFileUrl);
        fileRepository.save(newFile);

        /* ml에서 변환 예상 시간 받아오는 코드 작성 */
        int expected_sec = 300; // 임의로 지정

        return FilePostResponseDto.builder()
                .file_id(newFile.getId())
                .expected_sec(expected_sec)
                .build();
    }


//    @Autowired
//    public FileService(FileRepository fileRepository) {
//        this.fileRepository = fileRepository;
//        this.file = File.createFile(null, null, null);
//    }

}