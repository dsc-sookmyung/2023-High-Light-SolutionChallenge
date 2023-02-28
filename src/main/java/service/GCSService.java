package service;


import com.google.cloud.storage.Acl;
import com.google.cloud.storage.BlobInfo;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import dto.UploadReqDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

@Service
@RequiredArgsConstructor
public class GCSService {
    private Storage storage;
    @Value("${spring.cloud.gcp.bigquery.project-id}")
    private final String projectId;

    @SuppressWarnings("deprecation")
    public BlobInfo uploadFileToGCS(UploadReqDto uploadReqDto) throws IOException {
        storage = StorageOptions.newBuilder().setProjectId(projectId).build().getService();
        BlobInfo blobInfo = storage.create(
                BlobInfo.newBuilder(uploadReqDto.getBucketName(), uploadReqDto.getUploadFileName())
                        .setAcl(new ArrayList<>(Arrays.asList(Acl.of(Acl.User.ofAllAuthenticatedUsers(), Acl.Role.READER))))
                        .build(),
                new FileInputStream(uploadReqDto.getLocalFileLocation()));
        return blobInfo;
    }
}
