import 'package:dio/dio.dart';

class AuthDio{
  static const serverUrl = 'https://4cde304b-5a97-42e0-8233-5db2d54e8848.mock.pstmn.io';

  final dio = Dio(
    BaseOptions(
      baseUrl: serverUrl,
      connectTimeout: const Duration(seconds: 5000),
      receiveTimeout: const Duration(seconds: 3000)
    )
  );


  void setAuthToken (String token) {
    dio.options.headers["Authorization"] = "Bearer $token";
    print("header >>>> ${dio.options.headers.toString()}");
  }

  Future<Response> get(String url){
    return dio.get(url);
  }

  Future <Response> post(String url, Object data){
    return dio.post(url, data: data);
  }


}
