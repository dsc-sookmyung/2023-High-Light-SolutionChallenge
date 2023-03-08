import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
//import 'package:just_audio/just_audio.dart';
import 'package:leturn/component/UnitWidgets.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:leturn/models/textUnit.dart';
import '../models/imageUnit.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeLeft]);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    return ScreenUtilInit(
      designSize: Size(1180, 820),
      builder: (context, child) => MaterialApp(
        home: PageRead(),
      ),
    );
  }
}

class UnitList {
  final List<TextUnit> textList;
  List<ImageUnit>? imgList;
  final bool imgExist;

  UnitList({required this.textList, this.imgList, required this.imgExist});

  factory UnitList.fromJson(String jsonString) {
    List<dynamic> jsonResponse = json.decode(jsonString)["text"];
    List<dynamic> jsonResponse2 = json.decode(jsonString)["image"];

    List<TextUnit> textList = <TextUnit>[];
    textList = jsonResponse.map((t) => TextUnit.fromJson(t)).toList();

    if (jsonResponse2.isNotEmpty) {
      List<ImageUnit> imgList = <ImageUnit>[];
      imgList = jsonResponse2.map((e) => ImageUnit.fromJson(e)).toList();
      return UnitList(textList: textList, imgList: imgList, imgExist: true);
    }

    return UnitList(textList: textList, imgExist: false);
  }
}

class PageRead extends StatefulWidget {
  const PageRead({Key? key}) : super(key: key);

  @override
  _PageReadState createState() => _PageReadState();
}

class _PageReadState extends State<PageRead> {

  int fontBase = 0;
  double fileId = 2;
  int pageId = 5;
  //오디오 관련
  bool isPlaying = false;
  final player = AudioPlayer();


  late UnitList unitList;
  late List<TextUnit> _allTexts;
  late List<ImageUnit> _allImages;

  Future<UnitList> getList() async {
    final routeFromJsonFile = await rootBundle.loadString("sample.json");
    unitList = UnitList.fromJson(routeFromJsonFile);

    _allTexts = unitList.textList ?? <TextUnit>[];
    _allImages = unitList.imgList ?? <ImageUnit>[];

    return unitList;
  }

  Future setAudio(int idx) async{
    final audioplayer = AudioCache(prefix: 'assets/');
    final url = await audioplayer.load('text_${idx+1}');
    player.setUrl(url.path, isLocal: true);

  }

  @override
  void initState() {
    super.initState();
    getList();
    player.onPlayerStateChanged.listen((state) {
      setState((){
        isPlaying = state == PlayerState.PLAYING;
      });});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              _FixedTop(),
              Expanded(
                child: Container(
                    height: double.infinity,
                    color: Colors.white,
                    padding: EdgeInsets.only(left: 30.w, top: 10.w, right: 10.w),
                    child: FutureBuilder(
                        future: getList(),
                        builder: (BuildContext ctx, AsyncSnapshot snapshot) {
                          if (snapshot.data == null) {
                            //print(snapshot.data);
                            return Container(
                              child: const Center(
                                child: CircularProgressIndicator(),
                              ),);}
                          else {
                            if (_allImages.isEmpty) {
                              return textListView(_allTexts, fontBase, unitList.imgExist);}
                            else {
                              return Stack(
                                children: [
                                  textListView(_allTexts, fontBase, unitList.imgExist),
                                  Positioned(
                                      bottom: 0,
                                      left: 0,
                                      right: 0,
                                      height: 120.h,
                                      child: imgWidget(_allImages)),
                                ],
                              );}
                          }
                        })),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _FixedTop() {
    return Container(
      color: Colors.amber,
      height: 90.h,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.arrow_back_ios_new_outlined),
            iconSize: 44.w,
          ),
          CircleAvatar(
            radius: 30.w,
            child: IconButton(
              icon: Icon( //재생, 일시정지 변환
                  isPlaying ? Icons.pause : Icons.play_arrow
              ),
              iconSize: 50.w,
              onPressed: () async {
                /*if(isPlaying){
                  await player.pause();
                }else{
                  await player.resume();}*/
              },
            ),
          ),
          //재생 속도 조절바
          Container(

          ),
          Container(
            child: Row(
              children: [
                ButtonSemantics(
                  child: IconButton(
                    onPressed: () {},
                    icon: Icon(Icons.bookmarks),
                    iconSize: 44.w,
                  ),
                  excludeSemantics: false,
                  label: '북마크 모음',
                ),
                ButtonSemantics(
                  child: IconButton(
                    onPressed: () {},
                    icon: Icon(Icons.search),
                    iconSize: 44.w,
                  ),
                  excludeSemantics: false,
                  label: '페이지 이동',
                ),
                ButtonSemantics(
                  child: IconButton(
                    onPressed: () {},
                    icon: Icon(Icons.bookmark_border),
                    iconSize: 44.w,
                  ),
                  excludeSemantics: false,
                  label: '북마크 등록',
                )
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget textBlock(List<dynamic> _allTexts,int fontBase, int idx){
    return Material(
      color: Colors.transparent,
      child: InkWell(
        highlightColor: Colors.amberAccent,
        splashColor: Colors.amberAccent,
        onTap: () async{
          if(isPlaying){
            await player.pause();
            await player.dispose();
            setAudio(idx);
          }else{
            setAudio(idx);
            await player.resume();
            //await player.resume();
          }
        },
        child: Container(
          //color: Colors.orange,
          child: Text(
            _allTexts[idx].textLine,
            style: TextStyle(
                fontSize:
                _allTexts[idx].fontSize.toDouble() + fontBase),
          ),
        ),
      ),
    );
  }

  Widget textListView(List<dynamic> _allTexts, int fontBase, bool spacer) {
    return Container(
      //height: double.infinity,
      child: ListView.builder(
          itemCount: _allTexts.length,
          itemBuilder: (ctx, int idx) {
            if ((idx == _allTexts.length-1) && spacer) {
              //print(spacer);
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  textBlock(_allTexts, fontBase, idx),
                  Container(
                    //color:Colors.amber,
                    height: 110.h,
                    width: 200.w,
                  ),
                ],
              );
            }
            return textBlock(_allTexts, fontBase, idx);
          }),
    );
  }

  Widget imgWidget(List<ImageUnit>? allImages) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.only(
            topLeft: Radius.circular(30.w), topRight: Radius.circular(30.w)),
        color: Color(0x4d666666),
      ),
      child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemCount: allImages!.length,
          itemBuilder: (ctx, int idx) {
            return Container(
                margin: EdgeInsets.fromLTRB(20.w, 10.h, 30.w, 10.h),
                child: Image.asset(
                  allImages![idx].imgUrl,
                  width: 100.w,
                  height: 100.h,
                  fit: BoxFit.fill,
                ));
          }),
    );
  }

}
