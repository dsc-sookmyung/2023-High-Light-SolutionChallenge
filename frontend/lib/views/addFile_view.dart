import 'dart:convert';
import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/views/home_screen.dart';
import 'package:leturn/views/loading_view.dart';

class AddFileView extends StatefulWidget{
  final int folderId;

  const AddFileView({Key? key, required this.folderId}) :super(key: key);

  @override
  _AddFileViewState createState() => _AddFileViewState();
}

class _AddFileViewState extends State<AddFileView>{

  String setFileName = "";
  FilePickerResult? finalFile;
  late String savedFileName = "";
  bool check = false;
  late int fileId;

  Widget makeFilePicker(){
    return Center(
      child: Column(
       children: [
         Text('파일 선택',
           style: TextStyle(
             fontSize: 40.sp,
             fontWeight: FontWeight.w600,
             color: Colors.white,
           ),
           semanticsLabel: "파일 선택",),
         SizedBox(height: 10.h,),
         InkWell(
           onTap: () async{
             FilePickerResult? result = await FilePicker.platform.pickFiles(
               type: FileType.custom,
               allowedExtensions: ['pdf'],
             );
             if(result != null && result.files.isNotEmpty) {
               String fileName = result.files.first.name;
               //Uint8List fileBytes = result.files.first.bytes!;
               print("Filename>>> $fileName");
               //debugPrint(fileName);
               setState(() {
                 setFileName = fileName;
                 finalFile = result;
                 savedFileName = fileName;
               });
             }
           },
           child: Container(
             width: 700.w,
             height: 100.h,
             color: Colors.amberAccent,
             child: Center(
               child: Text(
                 setFileName,
                 style: TextStyle(
                   fontSize: 40.sp,
                   fontWeight: FontWeight.w800,
                   color: FONT_BLACK,
                 ),
                 semanticsLabel: setFileName,
               ),
             )
           ),
         ),
         SizedBox(width: 100.w, height: 100.h,),
         Text('저장명',
           style: TextStyle(
             fontSize: 40.sp,
             fontWeight: FontWeight.w600,
             color: Colors.white,
           ),
           semanticsLabel: "변환 파일 저장명",),
         SizedBox(height: 10.h,),
         Container(
             width: 700.w,
             height: 100.h,
             color: Colors.white,
             child: TextField(
               onChanged: (text){
                 if(text == null || text!.replaceAll(RegExp('\\s'), "").isEmpty){
                   setState(() {
                     savedFileName = setFileName;
                     check = true;
                   });
                 }else{
                   setState((){
                     check = false;
                     savedFileName = text;
                   });
                 }
               },
               decoration: InputDecoration(
                   border: InputBorder.none,
                   focusedBorder: InputBorder.none,
                 hintText: savedFileName,
                 fillColor: FONT_BLACK
               ),
               style: TextStyle(
                 fontWeight: FontWeight.w500,
                 fontSize: 40.sp
               ),
               textAlign: TextAlign.center,
               textAlignVertical: TextAlignVertical.center,
               inputFormatters: [FilteringTextInputFormatter.allow(RegExp(r'[a-z|A-Z|0-9|ㄱ-ㅎ|ㅏ-ㅣ|가-힣|ᆞ|ᆢ|ㆍ|ᆢ|ᄀᆞ|ᄂᆞ|ᄃᆞ|ᄅᆞ|ᄆᆞ|ᄇᆞ|ᄉᆞ|ᄋᆞ|ᄌᆞ|ᄎᆞ|ᄏᆞ|ᄐᆞ|ᄑᆞ|ᄒᆞ]'))],
             )
         ),
        Text(
          check ? '변환 명을 입력해주세요':'',
          style: TextStyle(
            fontSize: 37.sp,
            fontWeight: FontWeight.w800,
            color: Colors.redAccent,
            ),
          ),
       ],
      ),
    );
  }
  
  Future<void> sendFile(String changedName, int folderId) async{

    if(finalFile != null) {
      final filePath = finalFile!.files.single.path;
      
      var formData = FormData.fromMap({
        'file' : await MultipartFile.fromFile(filePath!),
        'fileName' : changedName,
        'folder_id' : folderId
      });

      final response = await dio.post('/folder/${widget.folderId}/files', formData);

      if(response.statusCode == 200){
        var data = response.data;
        fileId = data["data"]["file_id"];
        print("fileId = ${data["file_id"]}");
        print("saveFileName = $savedFileName");

      }
    }
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        backgroundColor: MAIN_YELLOW,
        toolbarHeight: 100.h,
        leading: IconButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          icon: Icon(Icons.arrow_back_ios_new, size: 64.h, color: Colors.black),
        ),
        title: Row(
            children: [
              SizedBox(width: 430.w,),
              Text('파일 변환',
                style: TextStyle(
                  fontSize: 40.sp,
                  fontWeight: FontWeight.w800,
                  color: FONT_BLACK,
                ),
                semanticsLabel: "파일 변환 페이지",),
            ],
          ),
        ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(height: 20.h,),
            Container(child: makeFilePicker()),
            FloatingActionButton(
              backgroundColor: Colors.transparent,

                child: Icon(
                  Icons.change_circle,
                  color: MAIN_YELLOW,
                  size: 80.w,
                ),
                onPressed: (){
                if(savedFileName.isEmpty){
                  print("비었음~~~~~");
                }else{
                  sendFile(savedFileName!, widget.folderId);
                  Navigator.of(context).pop();
                  Navigator.push(context, MaterialPageRoute(builder: (context)=> LoadingView(fileId: fileId)));
                  }
                }
            ),
          ],
        ),
      ),
    );
  }

}