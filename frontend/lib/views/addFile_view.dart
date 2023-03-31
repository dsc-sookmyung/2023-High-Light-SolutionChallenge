import 'dart:convert';
import 'dart:typed_data';
import 'package:http_parser/http_parser.dart';
import 'package:dio/dio.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:leturn/component/button_semantics.dart';
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
  String keepName = "";
  FilePickerResult? finalFile;
  late String savedFileName = "";
  bool check = false;
  int fileId =0;

  final textController = TextEditingController();
  List undetected_list = [" ", "`", "~", "!", "@", "#", "\$", "%", "^", "&", "*",
    "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "'", '"', ";", ":", "/", "?",
    ",", ".", "<", ">", "\\", "|", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"];
  List numberPad_list = ["Numpad Decimal", "Numpad Divide", "Numpad Multiply",
    "Numpad Subtract", "Numpad Add", "Numpad 0", "Numpad 1", "Numpad 2", "Numpad 3",
    "Numpad 4", "Numpad 5", "Numpad 6", "Numpad 7", "Numpad 8", "Numpad 9"];
  List numerPad_convert = [".", "/", "*", "-", "+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

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
               //print("Filename>>> $fileName");
               //debugPrint(fileName);
               setState(() {
                 setFileName = fileName.split('.')[0];
                 keepName = fileName;
                 finalFile = result;
                 savedFileName = fileName.split('.')[0];
               });
             }
           },
           child: Container(
             width: 700.w,
             height: 100.h,
             color: Colors.amberAccent,
             child: Center(
               child: Text(
                 keepName,
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
             child: textFieldCon(),
         ),
        Text(
          check ? '변환 명을 입력해주세요':'',
          style: TextStyle(
            fontSize: 37.sp,
            fontWeight: FontWeight.w800,
            color: Colors.redAccent,
            ),
          semanticsLabel: check ? '변환 명을 입력해주세요':'',
          ),
       ],
      ),
    );
  }

  Widget textFieldCon(){
    return RawKeyboardListener(
      focusNode: FocusNode(),
      onKey: (RawKeyEvent event) async {
        if (event.runtimeType == RawKeyDownEvent) {
          String keydownText = event.data.logicalKey.keyLabel;
          int cursorPosition = textController.selection.baseOffset;
          if (numberPad_list.contains(keydownText)) {
            keydownText = numerPad_convert[numberPad_list.indexOf(keydownText)];
          }
          if (undetected_list.contains(keydownText)) {
            await Future.delayed(Duration(milliseconds: 10));
            List text_list = textController.text.split("");
            try {
              if (text_list[cursorPosition] != keydownText) {
                text_list.insert(cursorPosition, keydownText);
                textController.text = text_list.join();
                textController.selection = TextSelection.fromPosition(TextPosition(offset: cursorPosition+1));
              }
            } catch (e) {
              if (text_list[textController.text.length-1] != keydownText) {
                textController.text = textController.text + keydownText;
                textController.selection = TextSelection.fromPosition(TextPosition(offset: textController.text.length));
              }
            }
          }
        }
      },
      child: TextField(
        controller: textController,
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
        keyboardType: TextInputType.name,
        style: TextStyle(
            fontWeight: FontWeight.w500,
            fontSize: 40.sp
        ),
        textAlign: TextAlign.center,
        textAlignVertical: TextAlignVertical.center,
        inputFormatters: [FilteringTextInputFormatter.allow(RegExp(r'[a-z|A-Z|0-9|ㄱ-ㅎ|ㅏ-ㅣ|가-힣|_|-|ㆍ|ᆢ|ᄀᆞ|ᄂᆞ|ᄃᆞ|ᄅᆞ|ᄆᆞ|ᄇᆞ|ᄉᆞ|ᄋᆞ|ᄌᆞ|ᄎᆞ|ᄏᆞ|ᄐᆞ|ᄑᆞ|ᄒᆞ]'))],
      ),
    );
  }
  Future<void> sendFile(String changedName, int folderId) async{

    if(finalFile != null) {
      final filePath = finalFile!.files.single.path;
      
      var formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(filePath!, contentType: MediaType('application', 'pdf')),
        'file_name': changedName
      });

      final response = await dio.postFile('/folder/${widget.folderId}/files', formData);

      if(response.statusCode == 200){
        var data = response.data["data"];
        fileId = data["file_id"];
        print("addFile//fileId = ${data["file_id"]}");
        print("data = $data");

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
        leading: ButtonSemantics(
          label: "뒤로 가기",
          child: IconButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            icon: Icon(Icons.arrow_back_ios_new, size: 64.h, color: Colors.black),
          ),
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
      body: GestureDetector(
        onTap: (){
          FocusScope.of(context).unfocus();
        },
        child: SingleChildScrollView(
          child: Column(
            children: [
              SizedBox(height: 20.h,),
              Container(child: makeFilePicker()),
              ButtonSemantics(
                label: "전환 시작 버튼",
                child: FloatingActionButton(
                  backgroundColor: Colors.transparent,
                    child: Icon(
                      Icons.change_circle,
                      color: MAIN_YELLOW,
                      size: 80.w,
                    ),
                    onPressed: () async {
                    if(savedFileName.isEmpty){
                      print("비었음~~~~~");
                    }else{
                      await sendFile(savedFileName!, widget.folderId);
                      Navigator.of(context).pop();
                      Navigator.push(context, MaterialPageRoute(builder: (context)=> LoadingView(fileId: fileId)));
                      }
                    }
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

}