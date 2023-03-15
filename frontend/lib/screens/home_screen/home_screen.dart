import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:leturn/api/google_signin_api.dart';
import 'package:leturn/const/colors.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:http/http.dart' as http;
import 'package:leturn/screens/page_view.dart';
import 'package:leturn/screens/login/login_page.dart';
import 'package:leturn/screens/user_folder.dart';

import '../../const/Server.dart';

var token;

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
    return Container(
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
                //bool result = nextPage();
                if(await nextPage()) {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => FolderPage()));
                }
              },
            ),
          ),
          //2. 카카오 로그인
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
                primary: Color(0xffFEE500),
                onPrimary: FONT_BLACK,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset(
                    'assets/Kakao.png',
                    height: 100.h,
                  ),
                  Container(
                    margin: EdgeInsets.only(left: 16.0.w),
                    child: Text(
                      'Kakao로 로그인 ',
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
    );
  }

  Future signIn() async{
    final GoogleSignInAccount? googleUser = await GoogleSignIn().signIn();
    final GoogleSignInAuthentication? googleAuth = await googleUser?.authentication;

    if(googleAuth == null) {
      print("google login error >>> googleAuth is null");
    }else{
      String url = '$serverHttp/login/google';
      //final req = jsonEncode(<String,String>{'access_token':googleAuth!.accessToken.toString()});
      final req = jsonEncode(<String,String>{'access_token':'accessToken'});

      http.Response response = await http.post(Uri.parse(url),body: req);

      if(response.statusCode == 200){
        token = jsonDecode(response.body)["token"];
        print("token : $token");
        //저장소에 토큰 저장
      }else{
        print(response.statusCode.toString());
      }
    }

  }

  Future<bool> nextPage() async{
    await signIn();
    if(token == null){
      return false;
    }else{
      return true;
    }
  }


}