package com.SollutionChallenge.HighLight.service;


import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.BlobInfo;
import com.google.cloud.storage.Storage;
import com.SollutionChallenge.HighLight.dto.UploadReqDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class GCSService {

    private final Storage storage;
    @Value("${spring.cloud.gcp.storage.bucket}")
    private String bucketName;

    public String uploadNewFile(UploadReqDto dto, Long folderId) throws IOException {
//        String uuid = UUID.randomUUID().toString(); // Google Cloud Storage에 저장될 파일 이름
        String ext = dto.getUploaded_file().getContentType(); // 파일의 형식 ex) JPG
        Long user_id = dto.getUser_id();
        String uploadFilePath = user_id+"/"+folderId+"/"+dto.getUploaded_file().getOriginalFilename();
        // Cloud에 이미지 업로드
        BlobInfo blobInfo = storage.create(
                BlobInfo.newBuilder(bucketName, uploadFilePath)
                        .setContentType(ext)
                        .build(),
                dto.getUploaded_file().getInputStream()
        );
        System.out.println("업로드 경로: " + uploadFilePath);
        return "https://storage.googleapis.com/"+bucketName+"/"+uploadFilePath;
    }





//    @SuppressWarnings("deprecation")
//    public BlobInfo uploadFileToGCS(UploadReqDto uploadReqDto) throws IOException {
//        storage = StorageOptions.newBuilder().setProjectId(projectId).build().getService();
//        BlobInfo blobInfo = storage.create(
//                BlobInfo.newBuilder(uploadReqDto.getBucketName(), uploadReqDto.getUploadFileName())
////                        .setAcl(new ArrayList<>(Arrays.asList(Acl.of(Acl.User.ofAllAuthenticatedUsers(), Acl.Role.READER))))
//                        .build(),
//                new FileInputStream(uploadReqDto.getLocalFileLocation()));
//        return blobInfo;
//    }


}
