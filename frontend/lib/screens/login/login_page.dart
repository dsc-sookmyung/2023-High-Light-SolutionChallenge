import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:leturn/const/colors.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class LoginPage extends StatelessWidget{
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        backgroundColor: PRIMARY_COLOR,
        toolbarHeight: 140.h,
        title: Text('로그인',
          style: TextStyle(
          color: MAIN_YELLOW,
          fontSize: 80.w,
          fontWeight: FontWeight.w800,)),
        leading: IconButton(
          onPressed: (){
            Navigator.of(context).pop();
          },
          icon: Icon(Icons.arrow_back_ios_new,
          )),
        systemOverlayStyle: SystemUiOverlayStyle.light,
      ),
      body: Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Container(
              height: 50.h,
            ),
            Container(
              color: Colors.lightBlue,
              width: 500.w,
              height: 80.h,
              child: ElevatedButton (
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15.0.w),
                  ),
                  primary: Colors.white,
                  onPrimary: FONT_BLACK,
                ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SvgPicture.asset(
                        'assets/Google.svg',
                        height: 100.h,
                      ),
                      Container(
                        margin: EdgeInsets.only(left: 16.0.w),
                        child: Text(
                          'Google로 로그인',
                          style: TextStyle(
                            color: FONT_BLACK,
                            fontSize: 40.sp,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      )
                    ],
                  ),
                  onPressed: (){},
              ),
            ),
          ],
        ),
      )
    );
  }
}