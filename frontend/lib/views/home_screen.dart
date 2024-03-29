import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:leturn/component/button_semantics.dart';
import 'package:leturn/const/colors.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:leturn/models/auth_dio.dart';
import 'package:leturn/views/library_view.dart';
import 'package:leturn/views/menu_page.dart';


final AuthDio dio = AuthDio();

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
    return ButtonSemantics(
      label: "구글 로그인 버튼",
      child: Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            //1. 구글 로그인
            Container(
              //color: Colors.lightBlue,
              width: 500.w,
              height: 90.h,
              margin: EdgeInsets.symmetric(vertical: 20.0.h),
              child: ElevatedButton (
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20.0.w),
                  ),
                  primary: Colors.white,
                  onPrimary: FONT_BLACK,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SvgPicture.asset(
                      'assets/Google.svg',
                      height: 80.h,
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
                onPressed: () async {
                  await signIn();
                  await Navigator.push(context, MaterialPageRoute(builder: (context) => LibraryView()));
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future signIn() async{
    final GoogleSignInAccount? googleUser = await GoogleSignIn().signIn();
    final GoogleSignInAuthentication? googleAuth = await googleUser?.authentication;

    if(googleAuth == null) {
      print("google login error >>> googleAuth is null");
    }else{
      final body = {'access_token' : googleAuth!.accessToken.toString()};
      print(body.toString());
      final response = await dio.post('/google/login', body);

      print("response?? ${response.data}");
      if(response.statusCode == 200){
        print(response.data);
        var data = response.data;
        //print("token_home_screen: $token");

        dio.setAuthToken(data["token"]);
      }else{
        print("mockserver_error: ${response.statusCode.toString()}");
      }
    }

  }



}