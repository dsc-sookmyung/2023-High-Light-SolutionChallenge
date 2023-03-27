package com.SollutionChallenge.HighLight.Page;

import com.SollutionChallenge.HighLight.File.*;
import com.SollutionChallenge.HighLight.User.Entity.User;
import com.SollutionChallenge.HighLight.User.UserRepository;
import com.SollutionChallenge.HighLight.auth.JwtTokenUtil;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Storage;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RequiredArgsConstructor
@Service
public class PageService {
    private final FileRepository fileRepository;
    private final UserRepository userRepository;
    @Autowired
    private Storage storage;
    @Transactional
    public SendPageResDto getPageContents(Long userId, Long fileId, Long pageId) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
//        User user = userRepository.findById(1L).get(); // api 테스트용 파일생성 코드 - 유저 정보 임의로 가져옴
        User user = userRepository.findById(userId).get();
        System.out.println("userid: "+userId);
//        File testfile = File.createFile(1L, user, "StallingsOS8e-Chap04", "파일링크"); // api 테스트용 파일 생성 코드
//        fileRepository.save(testfile); // api테스트용 파일 생성 코드

        // 파일 repository에서 파일 찾기
        Optional<File> wantedFile = fileRepository.findById(fileId);

        // GCS에서 해당하는 페이지 json 받아오기
        if (wantedFile.isPresent()) {
            File target = wantedFile.get();
            String fileName = target.getFileName();
//            String downloadFileName = "userid/"+fileName+"_json_folder/"+pageId+"/"+fileName+"_"+pageId+".json"; // api 테스트용 파일 생성 코드
            String downloadFileName = userId+"/"+fileName+"_json_folder/"+pageId+"/"+fileName+"_"+pageId+".json"; // 실제 코드

            System.out.println("다운로드 경로: " + downloadFileName);
            BlobId blobId = BlobId.of("cloud_storage_leturn", downloadFileName);
            Blob blob = storage.get(blobId);
            byte[] content = blob.getContent();
            String targetJson = new String(content, StandardCharsets.UTF_8);

            // 보내줄 형식 맞추어 다시 dto로 매핑하기
            GetPageResDto pageResDto = objectMapper.readValue(targetJson, GetPageResDto.class);
            List<TextInfoDto> textInfoDto = pageResDto.getText();
            List<SendTextInfoDto> sendTextInfoDto = new ArrayList<SendTextInfoDto>();
            for (TextInfoDto textDto: textInfoDto) {
                SendTextInfoDto sendDto = new SendTextInfoDto();
                sendDto.setText_content(textDto.getText());
                sendDto.setFont_size(textDto.getFont_size());
                sendDto.setAudio_url(textDto.getAudio_url());
                sendTextInfoDto.add(sendDto);
            }
            return SendPageResDto.builder()
                    .page_id(pageResDto.getPage_id())
                    .full_audio_url(pageResDto.getFull_text().getAudio_url())
                    .text(sendTextInfoDto)
                    .image(pageResDto.getImage())
                    .build();
        }
        else {
            return new SendPageResDto();
        }
    }
}
