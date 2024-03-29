import 'dart:convert';

import 'package:extended_image/extended_image.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/views/addFile_view.dart';
import 'package:leturn/views/open_file.dart';

import '../models/simpleFile.dart';
import 'home_screen.dart';

class FolderView extends StatefulWidget{
  final int folderId;
  final String folderName;

  const FolderView({
    Key? key, required this.folderId, required this.folderName}) : super(key: key);

  @override
  _FolderViewState createState() => _FolderViewState();

}

class _FolderViewState extends State<FolderView>{

  Future<List<SimpleFile>>? _files;
  late List<SimpleFile> exist = [];



  Future<List<SimpleFile>> _fetchData() async {
    final response = await dio.get('/folder/${widget.folderId}');

    if (response.statusCode == 200) {
      var data = response.data["data"];
      //파일 정보 파싱

      print("dd : ${widget.folderName}/${widget.folderId}");

      final List<dynamic> files = data["files"];
      exist = files.map((e) => SimpleFile.fromJson(e)).toList();
      return exist;
    } else {
      print("folder_view>>> error StatusCode : ${response.statusCode}");
      throw Exception('폴더 로드에 실패했습니다.');
    }
  }

  @override
  void initState(){
    super.initState();
    _files = _fetchData();
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
        //중간 부분
        title: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            //SizedBox(width: 350.w,),
            Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(width: 90.w,),
                  SvgPicture.asset(
                    'assets/opened_folder.svg',
                    height: 64.h,
                  ),
                  SizedBox(width: 30.w,),
                  Text(
                    widget.folderName,
                    style: TextStyle(
                      fontSize: 40.sp,
                      fontWeight: FontWeight.w800,
                      color: FONT_BLACK,
                    ),
                    semanticsLabel: widget.folderName,
                  ),
                ],
              ),
            )
          ],
        ),
        actions: [
          Padding(
            padding: EdgeInsets.all(5.h),
            child: ButtonSemantics(
              label: "파일 추가하기 버튼",
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context)
                  => AddFileView(folderId: widget.folderId)));

                },
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 5.h),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.0.w),
                  ),
                  primary: PRIMARY_COLOR,
                ),
                icon: Icon(Icons.add_circle,color: MAIN_YELLOW, size: 64.w,),
                label: Text(
                  '파일 추가',
                  style: TextStyle(
                    fontWeight: FontWeight.w500,
                    fontSize: 40.sp,
                    color: MAIN_YELLOW,
                  ),
                ),
              ),
            ),
          )
        ],
      ),
      body: Container(
        padding: EdgeInsets.only(top: 10.h),
        color: PRIMARY_COLOR,
        child: Center(
          child: FutureBuilder(
              future: _files,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  if(exist.isEmpty){
                    return Container(
                      padding: EdgeInsets.only(top: 320.h),
                      child: Center(
                        child: Text(
                          '폴더가 비었습니다',
                          style: TextStyle(
                            fontSize: 48.sp,
                            fontWeight: FontWeight.w700,
                            color: MAIN_YELLOW
                        ),
                          semanticsLabel: "폴더가 비었습니다",
                        ),
                      ),
                    );
                  }else{
                    return buildGridView(snapshot);
                  }
                } else if (snapshot.hasError) {
                  //print("error???? ${snapshot.error}");
                  return Text("SnapShot Error>>> ${snapshot.error}");
                } else {
                  return const Center(child: CircularProgressIndicator(color: MAIN_YELLOW,strokeWidth: 5,));
                }
              }),
        ),
      ),
    );
  }

  Widget buildGridView(snapshot) {
    return GridView.count(
        crossAxisCount: 3,
        physics: ScrollPhysics(),
        children: List.generate(
          snapshot.data!.length,
              (index) {
            return ButtonSemantics(
              label: "${snapshot.data![index].fileName}",
              child: Container(
                child: Center(
                  child: TextButton(
                    child: Column(
                      children: [
                        ExtendedImage.network(snapshot.data![index].fileImg,
                        fit: BoxFit.fitWidth),
                        Expanded(
                          child: Text(
                            snapshot.data![index].fileName,
                            style: TextStyle(fontSize: 44.sp, color: MAIN_YELLOW),
                            overflow: TextOverflow.fade,
                            softWrap: false,
                          ),
                        ),
                      ],
                    ),
                    onPressed: () {
                      Navigator.of(context).push(
                          MaterialPageRoute(builder: (context)
                          => BasePage(fileId: snapshot.data![index].fileId)));
                    },
                  ),
                ),
              ),
            );
          },
        ));
  }

}