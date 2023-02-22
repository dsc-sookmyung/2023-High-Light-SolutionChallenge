import 'package:flutter/material.dart';
import 'package:leturn/const/colors.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:leturn/screens/login/login_page.dart';

class HomeScreen extends StatelessWidget{
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: PRIMARY_COLOR,
      body: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(40.0),
            child: Row(
              children:const[
                Expanded(
                    child: _Logo()
                ),
                Expanded(
                    child: _Buttons()
                ),
              ],
            ),
          ) ),
    );
  }
}

class _Logo extends StatelessWidget{
  const _Logo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Image.asset(
        'assets/Leturn_logo.png',
        width: 400.w,
        height: 400.h,
      )
    );
  }
}

class _Buttons extends StatelessWidget{
  const _Buttons({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Expanded(
        child:
        Container(
          width: 400.w, height: 120.h, //color: Colors.orange,
          //margin: EdgeInsets.all(30),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20,60.0,20,20),
            child: ElevatedButton(
              onPressed: (){
                Navigator.push(context, MaterialPageRoute(
                    builder: (context) => LoginPage()));
              },
              style: ElevatedButton.styleFrom(
                primary: MAIN_YELLOW,
                onPrimary: FONT_BLACK,
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30.0.w)
                ),
                textStyle: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 70.sp,
                ),
                //padding: EdgeInsets.all(50.0),
              ),
              child: Text('로그인'),
            ),
        ),
        ),),
        Expanded(child: Container(
          width: 400.w, height: 120.h, //color: Colors.orange,
          //margin: EdgeInsets.all(30),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20,20,20,60),
            child: ElevatedButton(onPressed: (){},
              style: ElevatedButton.styleFrom(
                primary: MAIN_YELLOW,
                onPrimary: FONT_BLACK,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30.0.w)
                ),
                textStyle: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 70.sp,
                ),
                //padding: EdgeInsets.all(50.0),
              ),
              child: Text('회원가입'),
            ),
          ),
        ),
        ),
      ],
    );
  }
}