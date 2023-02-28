package dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@AllArgsConstructor
@Getter
@Setter
@Builder
public class UploadReqDto {
    private String bucketName;
    private String uploadFileName;
    private String localFileLocation;
}