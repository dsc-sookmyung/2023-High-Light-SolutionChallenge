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
    _subscription = Stream.periodic(Duration(seconds: 10)).listen((_) => _checkComplete());
  }

  @override
  void dispose(){
    _subscription.cancel();
    super.dispose();
  }

  Future<void> _checkComplete() async{
    try{
      final response = await dio.get('/conversion/status/${widget.fileId}');
      if(response.data['message'] == "Success"){
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


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: loading(),
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
                  size: 80.w,
                )
            ),
            SizedBox(height: 100.h,),
            Text("변환 중입니다...",
              style: TextStyle(
                  fontSize: 48.sp,
                  fontWeight: FontWeight.w700,
                color: MAIN_YELLOW
              ),)
          ],
        ),
      ),
    );
  }

}
