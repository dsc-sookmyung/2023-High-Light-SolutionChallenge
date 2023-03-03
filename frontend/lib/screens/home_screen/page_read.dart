import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:just_audio/just_audio.dart';


class PageRead extends StatefulWidget {
  const PageRead({Key? key}) : super(key: key);

  @override
  _PageReadState createState() => _PageReadState();
}

class _PageReadState extends State<PageRead> {

  //오디오 재생 위젯
  final _player = AudioPlayer();
  bool isPlaying = false;

  @override
  void initState(){
    super.initState();
    _init();
  }

  void _init(){
    _player.setAudioSource(AudioSource.uri(Uri()));
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
              Container(
                  child: Text('data\n hey~~~')
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
            onPressed:(){},
            icon: const Icon(Icons.arrow_back_ios_new_outlined),
            iconSize: 44.w,
          ),
          Container(
            child: Row(
              children: [
                ButtonSemantics(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(Icons.bookmarks),
                    iconSize: 44.w,
                  ),
                  excludeSemantics: false,
                  label: '북마크 모음',
                ),
                ButtonSemantics(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(Icons.search),
                    iconSize: 44.w,
                  ),
                  excludeSemantics: false,
                  label: '페이지 이동',
                ),
                ButtonSemantics(
                  child: IconButton(
                    onPressed: (){},
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


}