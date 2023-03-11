//1. 파일을 선택하면 해당 (파일의 고유번호) 와 페이지 총 개수를 response에 받아옴
//2. 받은 페이지 총 수를 기준으로 페이지 넘버 리스트를 생성, [1, 2, 3, ..., 54]해 베이스 페이지인 여기에 세팅함
//3. .Swiper 사용해 (future builder?) 각 페이지를 페이지 번호를 준 상태로 생성하고, 넘길 때 비로소 다음 페이지가 소환되도록?
//일단 그럼 페이지 단위의 생성자를 key외에 page_id를 추가 해야 겠다 그래야 required로
import 'dart:convert';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:card_swiper/card_swiper.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:leturn/const/Server.dart';
import 'package:leturn/screens/page_view.dart';
import 'package:logger/logger.dart';


void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: Size(1180, 820),
      builder: (context, child) =>
          MaterialApp(
            home: BasePage(fileId: 1),
          ),
    );
  }
}

var logger = Logger();

class BasePage extends StatefulWidget {

  final double fileId;

  const BasePage({
    Key? key,
    required this.fileId
  }) : super(key: key);

  ///*final*/double fileId = 1;

  @override
  _BasePageState createState() => _BasePageState();

}

class _BasePageState extends State<BasePage> with SingleTickerProviderStateMixin{


  late int totalPage;
  late List<int> pagesList = [];

  Future<void> getTotalPage(double fileId) async {
/*    late var url;

    Map<String, String> _params = <String,String> {
      'fileId' : fileId.toString(),
    };

    url = Uri.http('${serverHttp}', '/user', _params);*/
    String url = '${serverHttp}/user?fileId=${fileId}';

    //get 요청 보내고 response로 받아오기
    var response = await http.get(Uri.parse(url), headers: {
      'Accept' : 'application/json',
      "content-type" : "application/json",
      "Authorization" : "Bearer {token}"
    });

    //response의 state 체크
    if (response.statusCode == 200){
      //print('Response body: ${jsonDecode(utf8.decode(response.bodyBytes))}');
      var data = jsonDecode(response.body);
      //1. 총 페이지 수 오는 경우
      /*totalPage = data["pages"];
      if (totalPage < 1){
        logger.e("total<0 ---> totalPage : $totalPage");
      }
      setState((){
        pagesList = List.generate(totalPage, (i) => i+1);
      });*/
      setState(() {
        pagesList = List<int>.from(data["pages"]);
      });

    }
    //statusCode 이상한 경우 -> token 체크하는 코드 삽입
    /*else{
      logger.e("http통신 이상해 : ${response.statusCode}");
    }
    return pagesList;*/
  }

  @override
  void initState() {
    super.initState();
    getTotalPage(widget.fileId);
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: pagesList.isEmpty
        ? Container(child: CircularProgressIndicator(),)
        : Swiper(
          loop: false,
          itemBuilder: (BuildContext context, int idx){
            return ViewPage(fileId: widget.fileId, pageId: idx+1);
          },
          itemCount: pagesList.length,
          //pagination: SwiperPagination(),
          //control: SwiperControl(),
        ),

    );
  }
}