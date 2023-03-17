import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/const/Server.dart';
import 'package:leturn/screens/home_screen/home_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: Size(1180, 820),
      builder: (context, child) =>
          const MaterialApp(
            home: MenuScreen(),
          ),
    );
  }
}


class MenuScreen extends StatelessWidget {
  const MenuScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: PRIMARY_COLOR,
      body: SafeArea(
          child: MenuButtons(),
      ),
    );
  }

  Widget MenuButtons(){
    return Container(
      //alignment: Alignment.center,
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            //1. 내 서재
            Container(
              width: 400.w,
              height: 220.h,
              padding: EdgeInsets.all(20.h),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20.0.w),
                  ),
                  primary: MAIN_YELLOW,
                  //onPrimary: FONT_BLACK,
                ),
                child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SvgPicture.asset(
                      'assets/bookshelf.svg',
                      height: 64.h,
                    ),
                    Container(
                      margin: EdgeInsets.only(left: 16.0.w),
                      child: Text(
                        '내 서재',
                        style: TextStyle(
                          color: FONT_BLACK,
                          fontSize: 40.sp,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    )
                  ],
                ),
                onPressed: (){},
              ),
            ),
            //2. 파일 추가
            Container(
              width: 400.w,
              height: 220.h,
              padding: EdgeInsets.all(20.h),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20.0.w),
                  ),
                  primary: MAIN_YELLOW,
                  //onPrimary: FONT_BLACK,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SvgPicture.asset(
                      'assets/circle_plus.svg',
                      height: 64.h,
                    ),
                    Container(
                      margin: EdgeInsets.only(left: 16.0.w),
                      child: Text(
                        '파일 추가',
                        style: TextStyle(
                          color: FONT_BLACK,
                          fontSize: 40.sp,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    )
                  ],
                ),
                onPressed: (){
                  //String token1 = client.client.printHeader();
                  //print("path1 : $token1");
                },
              ),
            )
          ],
        ),
      ),
    );
  }


}