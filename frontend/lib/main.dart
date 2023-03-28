import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/views/home_screen.dart';

void main() {
  runApp(MyApp());
  WidgetsFlutterBinding.ensureInitialized();
  //화면 가로 고정
  //SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeLeft]);
  //풀화면 (로테이션 불가능)
  //SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);*/
}

class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeLeft]);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    return ScreenUtilInit(

      designSize: Size(1180, 820),
      builder: (context ,child) => MaterialApp(
        debugShowCheckedModeBanner: false,
        localizationsDelegates: [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        supportedLocales: [
          Locale('ko'),
        ],
        theme: ThemeData(
          scaffoldBackgroundColor: PRIMARY_COLOR,
          fontFamily: 'OnGothic'
        ),
        home: HomeScreen(),
      ),
    );
  }
}
