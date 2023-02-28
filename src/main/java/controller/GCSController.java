package controller;

import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobInfo;
import com.google.cloud.storage.Storage;
import dto.UploadReqDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import service.GCSService;

import java.io.IOException;

@RestController
@RequiredArgsConstructor
public class GCSController {
    @Autowired
    private GCSService gcsService;
    @Autowired
    private Storage storage;

    @PostMapping("/users/{user_id}/files")
    public ResponseEntity localUploadToStorage(@RequestBody UploadReqDto uploadReqDto) throws IOException {

        BlobInfo fileFromGCS = gcsService.uploadFileToGCS(uploadReqDto);
        return ResponseEntity.ok(fileFromGCS.toString());
    }

}
