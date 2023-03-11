package com.SollutionChallenge.HighLight.service;


import com.google.cloud.storage.BlobInfo;
import com.google.cloud.storage.Storage;
import com.SollutionChallenge.HighLight.dto.UploadReqDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class GCSService {

    private final Storage storage;
    @Value("${spring.cloud.gcp.storage.bucket}")
    private String bucketName;

    public void uploadNewImage(UploadReqDto dto) throws IOException {
        String uuid = UUID.randomUUID().toString(); // Google Cloud Storage에 저장될 파일 이름
        String ext = dto.getImage().getContentType(); // 파일의 형식 ex) JPG

        // Cloud에 이미지 업로드
        BlobInfo blobInfo = storage.create(
                BlobInfo.newBuilder(bucketName, uuid)
                        .setContentType(ext)
                        .build(),
                dto.getImage().getInputStream()
        );



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
