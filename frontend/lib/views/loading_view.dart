import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'dart:async';
import 'package:leturn/const/colors.dart';
import 'package:leturn/views/home_screen.dart';
import 'package:leturn/views/open_file.dart';

class LoadingView extends StatefulWidget{
  final int fileId;
  const LoadingView({Key? key, required this.fileId}) :  super (key: key);

  @override
  _LoadingViewState createState() => _LoadingViewState();

}


class _LoadingViewState extends State<LoadingView>{

  bool _isCompleted = false;
  late StreamSubscription _subscription;

  @override
  void initState(){
    super.initState();
    //_subscription = Stream.periodic(Duration(seconds: 10)).listen((_) => _checkComplete());
  }

  @override
  void dispose(){
    //_subscription.cancel();
    super.dispose();
  }

  Future<void> _checkComplete() async{
    try{
      final response = await dio.get('/conversion/status/${widget.fileId}');
      print("??? $response");
      if(response == "true"){
        setState(() {
          _isCompleted = true;
        });
        Navigator.pop(context);
        Navigator.push(context, MaterialPageRoute(builder: (context) => BasePage(fileId: widget.fileId)));
      }
    }catch(e){
      print(e);
    }
  }
  
  Widget _pass() {
    Future.delayed(const Duration(minutes: 5),(){
      print("loading <> ${widget.fileId}");
      Navigator.pop(context);
      Navigator.push(context, MaterialPageRoute(builder: (context) => BasePage(fileId: widget.fileId)));
    });
    return loading();
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pass(),
    );
  }

  Widget loading() {
    return Container(
      color: PRIMARY_COLOR,
      child: Center(
        child: Column(
          children: [
            SizedBox(height: 300.h,),
            Center(
                child: SpinKitCubeGrid(
                  color: MAIN_YELLOW,
                  size: 90.w,
                )
            ),
            SizedBox(height: 100.h,),
            Center(
              child: Text("변환 중입니다...\n평균 10분가량 소요 됩니다.",
                textAlign: TextAlign.center,
                style: TextStyle(
                    fontSize: 48.sp,
                    fontWeight: FontWeight.w700,
                  color: MAIN_YELLOW
                ),
                semanticsLabel: "변환 중입니다...  평균 10분가량 소요 됩니다.",
              ),
            )
          ],
        ),
      ),
    );
  }

}
