import 'dart:convert';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:card_swiper/card_swiper.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/views/home_screen.dart';
import 'package:leturn/views/pages/page_view.dart';
import 'package:logger/logger.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: Size(1180, 820),
      builder: (context, child) => MaterialApp(
        home: BasePage(fileId: 1),
      ),
    );
  }
}

var logger = Logger();

class BasePage extends StatefulWidget {
  final int fileId;

  const BasePage({Key? key, required this.fileId}) : super(key: key);

  @override
  _BasePageState createState() => _BasePageState();
}

class _BasePageState extends State<BasePage>
    with SingleTickerProviderStateMixin {
  //스와이퍼를 적용 vsync

  AudioPlayer player = AudioPlayer();
  num fontBase = 0;
  bool isPlaying = false;
  double playSpeed = 1.0;

  Future<int>? totalPage;
  int pageIdx = 0;

  void onPageChanged(int idx) async {
    if (pageIdx != idx) {
      await player.stop();
      player = AudioPlayer();
      setState(() {
        isPlaying = false;
        pageIdx = idx;
      });
    }
  }

  onScaleUpdate(ScaleUpdateDetails details) {
    setState(() {
      fontBase = details.scale.clamp(1.0, 5.0);
    });
  }
  isPlayingTrue(){
    setState(() {
      isPlaying = true;
    });
  }

  Future<int> getTotalPage(int fileId) async {
    final response = await dio.get('/files/$fileId');
    if (response.statusCode == 200) {
      var data = jsonDecode(response.data)["data"];
      print("pages>>>> ${data["page_num"]}");
      return data["page_num"];
    } else {
      print("open_file >>> error StatusCode : ${response.statusCode}");
      throw Exception("파일 열기에 실패했습니다.");
    }
    //print("pageList>>>>>$pagesList");
    //statusCode 이상한 경우 -> token 체크하는 코드 삽입
    /*else{
      logger.e("http통신 이상해 : ${response.statusCode}");
    }*/
  }

  @override
  void initState() {
    super.initState();
    totalPage = getTotalPage(widget.fileId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          _FixedTop(),
          Expanded(
            child: FutureBuilder(
                future: totalPage,
                builder: (context, AsyncSnapshot snapshot) {
                  print(snapshot.data);
                  print(totalPage);
                  if (snapshot.hasData) {
                    print(snapshot.data);
                    return Swiper(
                      loop: false,
                      itemCount: snapshot.data!,
                      itemBuilder: (BuildContext context, int idx) {
                        return ViewPage(
                            fileId: widget.fileId, pageId: idx + 1, player: player,
                        fontBase: fontBase, onScaleUpdate: onScaleUpdate, isPlayingTrue: isPlayingTrue,);
                      },
                      onIndexChanged: onPageChanged,
                    );
                  } else if (snapshot.hasError) {
                    return Text("snapshot Error>>> ${snapshot.error}");
                  } else {
                    return const Center(
                        child: CircularProgressIndicator(color: MAIN_YELLOW, strokeWidth: 5));
                  }
                }),
          ),
        ],
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
            onPressed: () {Navigator.of(context).pop();},
            icon: const Icon(Icons.arrow_back_ios_new_outlined),
            iconSize: 60.w,
          ),
          IconButton(
            iconSize: 50.w,
            onPressed: () async {
              if (player.playing) {
                setState(() {
                  isPlaying = false;
                });
                await player.pause();
              } else {
                setState(() {
                  isPlaying = true;
                });
                await player.play();
              }
              //print("isPlaying: $isPlaying");
            },
            icon: Icon(isPlaying ? Icons.pause_circle : Icons.play_circle,
                color: Colors.black),
          ),
          //재생 속도 조절바
          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              IconButton(
                onPressed: () async {
                  setState(() {
                    playSpeed = (playSpeed - 0.1).clamp(0.5, 2.0);
                  });
                  await player.setSpeed(playSpeed);
                },
                icon: Icon(Icons.remove_circle, size: 60.w, color: Colors.black,),
              ),
              Text(
                '${playSpeed.toStringAsFixed(1)}x',
                style: TextStyle(fontSize: 50.sp, fontWeight: FontWeight.w700, backgroundColor: Colors.white),
              ),
              IconButton(
                onPressed: () async {
                  setState(() {
                    playSpeed = (playSpeed + 0.2).clamp(0.5, 2.0);
                  });
                  await player.setSpeed(playSpeed);
                },
                icon: Icon(Icons.add_circle, size: 60.w, color: Colors.black,),
              ),
            ],
          ),
          Container(
            child: Row(
              children: [
                ButtonSemantics(
                  excludeSemantics: false,
                  label: '페이지 이동',
                  child: IconButton(
                    onPressed: () {},
                    icon: Icon(Icons.search),
                    iconSize: 60.w,
                  ),
                ),
                ButtonSemantics(
                  excludeSemantics: false,
                  label: '북마크 모음',
                  child: IconButton(
                    onPressed: () {},
                    icon: const Icon(Icons.bookmarks),
                    iconSize: 60.w,
                  ),
                ),
                ButtonSemantics(
                  excludeSemantics: false,
                  label: '북마크 등록',
                  child: IconButton(
                    onPressed: () {},
                    icon: Icon(Icons.bookmark_border),
                    iconSize: 60.w,
                  ),
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}
