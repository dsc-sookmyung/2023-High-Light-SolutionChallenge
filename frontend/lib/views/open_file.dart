import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:card_swiper/card_swiper.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/views/folder_view.dart';
import 'package:leturn/views/home_screen.dart';
import 'package:leturn/views/pages/pages_view.dart';
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

  SwiperController swiperController = SwiperController();
  late FToast fToast;
  AudioPlayer player = AudioPlayer();
  num fontBase = 20;
  bool? isPlaying = false;
  double playSpeed = 1.0;
  Map<int, String> fullAudio = {};
  //StreamSubscription? _playerSubscription;
  //late Timer? _timer;

  Future<int>? totalPage;
  late int totalItems;
  int pageIdx = 0;

  showLastPageToast() {
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: MAIN_YELLOW,
      ),
      child: Text(
        "마지막 페이지 입니다.",
        semanticsLabel: "마지막 페이지 입니다.",
        style: TextStyle(fontSize: 44.sp, fontWeight: FontWeight.bold),
      ),
    );

    fToast.showToast(
      child: toast,
      gravity: ToastGravity.CENTER,
      toastDuration: const Duration(seconds: 2),
    );
  }

  void onPageChanged(int idx) async {
    if (pageIdx != idx) {
      await player.stop();
      player = AudioPlayer();
      setState(() {
        isPlaying = false;
        pageIdx = idx;
        if (pageIdx == totalItems - 1) {
          showLastPageToast();
        }
      });
    }
  }

  onScaleUpdate(ScaleUpdateDetails details) {
    setState(() {
      fontBase = 10 * details.scale.clamp(2.0, 4.0);
    });
  }

  updateFullUrl(String url) async {
    fullAudio[pageIdx] = url;
  }

  isPlayingTrue() {
    setState(() {
      isPlaying = true;
    });
  }

  Future<int> getTotalPage(int fileId) async {
    final response = await dio.get('/files/$fileId');
    if (response.statusCode == 200) {
      var data = response.data["data"];
      print("data>>>> ${data}");
      totalItems = data["page_count"];
      return data["page_count"];
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
    fToast = FToast();
    fToast.init(context);

  }

  @override
  void dispose(){
    //_playerSubscription!.cancel();
    //_timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Expanded(
            child: FutureBuilder(
                future: totalPage,
                builder: (context, AsyncSnapshot snapshot) {
                  //print(snapshot.data);
                  //print(totalPage);
                  if (snapshot.hasData) {
                    //print(snapshot.data);
                    return Column(
                      children: [
                        _FixedTop(),
                        Expanded(
                          child: Swiper(
                            controller: swiperController,
                            loop: false,
                            itemCount: snapshot.data!,
                            itemBuilder: (BuildContext context, int idx) {
                              return ViewPage(
                                fileId: widget.fileId,
                                pageId: idx + 1,
                                player: player,
                                fontBase: fontBase,
                                onScaleUpdate: onScaleUpdate,
                                isPlayingTrue: isPlayingTrue,
                                updateFullUrl: updateFullUrl,
                              );
                            },
                            onIndexChanged: onPageChanged,
                          ),
                        ),
                      ],
                    );
                  } else if (snapshot.hasError) {
                    return Text("snapshot Error>>> ${snapshot.error}");
                  } else {
                    return const Center(
                        child: CircularProgressIndicator(
                            color: MAIN_YELLOW, strokeWidth: 5));
                  }
                }),
          ),
        ],
      ),
    );
  }

  Widget _FixedTop() {
    return SafeArea(
      child: Container(
        color: Colors.amber,
        height: 90.h,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                ButtonSemantics(
                  label: "뒤로 가기",
                  child: IconButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    icon: const Icon(Icons.arrow_back_ios_new_outlined),
                    iconSize: 60.w,
                  ),
                ),
                SizedBox(width: 10.w,),
                Row(
                  children: [
                    Padding(
                      padding: EdgeInsets.all(2.h),
                      child: ElevatedButton(
                        onPressed: () async {
                          isPlayingTrue();
                          await player.setUrl(fullAudio[pageIdx]!);
                          await player.play();
                        },
                        style: ElevatedButton.styleFrom(
                          //padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 5.h),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10.0.w),
                          ),
                          primary: PRIMARY_COLOR,
                        ),
                        child: Text(
                          '전체 듣기',
                          style: TextStyle(
                            fontWeight: FontWeight.w700,
                            fontSize: 42.sp,
                            color: MAIN_YELLOW,
                          ),
                        ),
                      ),
                    ),
                    StreamBuilder<PlayerState>(
                      stream: player.playerStateStream,
                      builder: (_, snapshot){
                        final playerState = snapshot.data;
                        return _playPauseButton(playerState);
                      },
                    ),
                  ],
                ),
              ],
            ),
            //SizedBox(width: 40.w,),
            //재생 속도 조절바
            Row(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    SizedBox(
                      height: double.infinity,
                      child: ButtonSemantics(
                        label: "재생속도 마이너스 영점일",
                        child: IconButton(
                          onPressed: () async {
                            setState(() {
                              playSpeed = (playSpeed - 0.1).clamp(0.5, 2.5);
                            });
                            await player.setSpeed(playSpeed);
                          },
                          icon: Icon(
                            Icons.remove_circle,
                            size: 64.w,
                            color: Colors.black,
                          ),
                        ),
                      ),
                    ),
                    SizedBox(
                      width: 30.w,
                    ),
                    Container(
                      decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(10.0.w),
                          color: Colors.white
                      ),
                      child: Text(
                        '${playSpeed.toStringAsFixed(1)}x',
                        semanticsLabel: "재생속도 ${playSpeed.toStringAsFixed(1)}",
                        style: TextStyle(
                            fontSize: 50.sp,
                            fontWeight: FontWeight.w700,
                            backgroundColor: Colors.white),
                      ),
                    ),
                    SizedBox(
                      height: double.infinity,
                      child: ButtonSemantics(
                        label: "재생속도 플러스 영점일",
                        child: IconButton(
                          onPressed: () async {
                            setState(() {
                              playSpeed = (playSpeed + 0.1).clamp(0.5, 2.5);
                            });
                            await player.setSpeed(playSpeed);
                          },
                          icon: Icon(
                            Icons.add_circle,
                            size: 64.w,
                            color: Colors.black,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(width: 50.w,),
                Container(
                  child: Row(
                    children: [
                      SizedBox(
                        height: 75.h,
                        width: 70.w,
                        child: ButtonSemantics(
                          label: "5페이지 전으로 이동",
                          child: IconButton(
                            icon: SvgPicture.asset(
                              'assets/left_icon.svg',
                            ),
                            onPressed: (){
                              setState(() {
                                if(pageIdx >= 5){
                                  pageIdx -= 5;
                                }else{
                                  pageIdx = 0;
                                }
                                swiperController.move(pageIdx);
                              });
                            },
                          ),
                        ),
                      ),
                      Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(10.0.w),
                          color: Colors.white
                        ),
                        child: Text(
                          '${pageIdx+1} / $totalItems pages',
                          semanticsLabel: "총 $totalItems 페이지 중 현재 ${pageIdx+1} 페이지",
                          style: TextStyle(
                              fontSize: 50.sp,
                              fontWeight: FontWeight.w700,
                             ),
                        ),
                      ),
                      SizedBox(
                        height: 75.h,
                        width: 70.w,
                        child: ButtonSemantics(
                          label: "5페이지 후로 이동",
                          child: IconButton(
                            icon: SvgPicture.asset('assets/right_icon.svg',
                                height: 64.w,
                            ),
                            onPressed: (){
                              setState(() {
                                if(pageIdx <= (totalItems! - 5)){
                                  pageIdx += 5;
                                }else{
                                  pageIdx = totalItems-1;
                                }
                                swiperController.move(pageIdx);
                              });
                            },
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _playPauseButton(PlayerState? playerState) {
    final processingState = playerState?.processingState;
    if (processingState == ProcessingState.loading ||
        processingState == ProcessingState.buffering) {
      return ButtonSemantics(
        label: "일시정지",
        child: IconButton(
          icon: Icon(Icons.pause_circle),
          iconSize: 64.w,
          onPressed: player.pause,
        ),
      );
    } else if (player.playing != true) {
      return ButtonSemantics(
        label: "재생",
        child: IconButton(
          icon: Icon(Icons.play_circle),
          iconSize: 64.w,
          onPressed: player.play,
        ),
      );
    } else if (processingState != ProcessingState.completed) {
      return ButtonSemantics(
        label: "일시정지",
        child: IconButton(
          icon: Icon(Icons.pause_circle),
          iconSize: 64.w,
          onPressed: player.pause,
        ),
      );
    } else {
      return ButtonSemantics(
        label: "재생",
        child: IconButton(
          icon: Icon(Icons.play_circle),
          iconSize: 64.w,
          onPressed: player.play,
        ),
      );
    }
  }

}

