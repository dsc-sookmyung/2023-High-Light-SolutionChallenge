import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/models/folders.dart';
import 'package:leturn/views/folder_view.dart';
import 'package:leturn/views/home_screen.dart';

class LibraryView extends StatefulWidget {
  const LibraryView({Key? key}) : super(key: key);

  @override
  _LibraryViewState createState() => _LibraryViewState();
}

class _LibraryViewState extends State<LibraryView> {
  Future<List<Folders>>? _folders;
  late FToast fToast;

  showCustomToast() {
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.redAccent,
      ),
      child: Text("폴더명을 입력하세요", style: TextStyle(fontSize: 44.sp, fontWeight: FontWeight.bold),),
    );

    fToast.showToast(
      child: toast,
      gravity: ToastGravity.TOP,
      toastDuration: Duration(seconds: 2),
    );
  }

  @override
  void initState() {
    super.initState();
    _folders = _fetchData();
    fToast = FToast();
    fToast.init(context);
  }

  Future<List<Folders>> _fetchData() async {

    final response = await dio.get('/folders');

    if (response.statusCode == 200) {
      var data = jsonDecode(response.data)["data"];
      //print(data);
      final List<dynamic> folders = data["folder"];
      return folders.map((element) => Folders.fromJson(element)).toList();
    } else {
      print("lib_view>>> error StatusCode : ${response.statusCode}");
      throw Exception('서재 로드에 실패했습니다.');
    }
  }

  Future<List<Folders>> _sendData(String folderName) async {

    Map<String, String> body = {'folder_name': folderName};
    final response = await dio.post('/folders', body);

    //final response = await client.post(Uri.parse(url), body: jsonEncode(body));
    if (response.statusCode != 200) {
      //logger.e("statusCode2 >>> ${response.statusCode}");
      print("error StatusCode : ${response.statusCode}");
      throw Exception('폴더 생성에 실패했습니다.');
    } else {
      var data = jsonDecode(response.data)["data"];
      final List<dynamic> folders = data["folder"];
      return folders.map((element) => Folders.fromJson(element)).toList();
    }
  }

  void folderDialog() {
    showDialog(
        context: context,
        barrierDismissible: true,
        builder: (BuildContext context1) {
          String? input;
          return AlertDialog(
            insetPadding: EdgeInsets.symmetric(horizontal: 40.w, vertical: 20.h),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10.0.w),
            ),
            title: Text(
              "폴더 추가",
              style: TextStyle(fontSize: 44.sp, fontWeight: FontWeight.bold),
            ),
            content: Container(
              child: TextField(
                onChanged: (text) {
                  input = text;
                },
                decoration: InputDecoration(hintText: '폴더명을 입력하세요'),
              ),
            ),
            actions: [
              ElevatedButton(
                child: const Text('확인'),
                onPressed: () async {
                  if (input == null ||
                      input!.replaceAll(RegExp('\\s'), "").isEmpty) {
                    showCustomToast();
                    return;
                  } else {
                    List<Folders> folders = await _sendData(input!);
                    //print("input: $input");
                    //print("renew List : ${folders.toString()}");
                    setState(() {
                      _folders = Future.value(folders);
                    });
                    Navigator.of(context).pop();
                  }
                },
              )
            ],
          );
        });
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
        //중간 부분
        title: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            SizedBox(width: 380.w,),
            SvgPicture.asset(
              'assets/bookshelf.svg',
              height: 64.h,
            ),
            SizedBox(width: 30.w,),
            Text(
              "내 서재",
              style: TextStyle(
                fontSize: 40.sp,
                fontWeight: FontWeight.w800,
                color: FONT_BLACK,
              ),
              semanticsLabel: "내 서재",
            )
          ],
        ),
        actions: [
          Padding(
            padding: EdgeInsets.all(5.h),
            child: ElevatedButton.icon(
              onPressed: () {
                folderDialog();
              },
              style: ElevatedButton.styleFrom(
                //padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 5.h),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0.w),
                ),
                primary: PRIMARY_COLOR,
              ),
              icon: Icon(Icons.add_circle,color: MAIN_YELLOW, size: 64.w,),
              label: Text(
                '폴더 추가',
                style: TextStyle(
                  fontWeight: FontWeight.w700,
                  fontSize: 40.sp,
                  color: MAIN_YELLOW,
                ),
              ),
            ),
          )
        ],
      ),
      body: SafeArea(
        child: Container(
          color: PRIMARY_COLOR,
          child: FutureBuilder(
            future: _folders,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                return buildListView(snapshot);
              } else if (snapshot.hasError) {
                //print("error???? ${snapshot.error}");
                return Text("error? ${snapshot},${snapshot.error}");
              } else {
                return const Center(child: CircularProgressIndicator(color: MAIN_YELLOW,strokeWidth: 5,));
              }
            }),
        ),
      ),
    );
  }


  Widget buildListView(snapshot){
    return ListView.separated(
      scrollDirection: Axis.vertical,
        padding: EdgeInsets.only(top: 15.h,left: 15.w, right: 15.w),
        separatorBuilder: (BuildContext context, int idx) => const Divider(color: Colors.grey, thickness: 2),
        itemCount: snapshot.data!.length,
        itemBuilder: (BuildContext context, int idx){
          return TextButton(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Icon(Icons.folder, size: 80.w, color: MAIN_YELLOW,),
                SizedBox(width: 30.w,),
                Expanded(
                  child: Text(
                    snapshot.data![idx].folderName,
                    style: TextStyle(fontSize: 65.sp, color: MAIN_YELLOW),
                    maxLines: 1,
                    softWrap: false,
                    overflow: TextOverflow.ellipsis,
                  ),
                )
              ],
            ),
            onPressed: (){
              Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => FolderView(folderId: snapshot.data![idx].folderId, folderName: snapshot.data![idx].folderName)));},
          );
        }
    );
  }

}
