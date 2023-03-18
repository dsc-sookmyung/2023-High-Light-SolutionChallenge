import 'package:http/http.dart';
import 'dart:convert';
import 'dart:async';
import 'dart:io';

class MClient extends BaseClient {
  Map<String, String> _defaultHeader = {};
  final Client _client = Client();

  MClient();

  @override
  Future<StreamedResponse> send(BaseRequest request) {
    return _client.send(request);
  }

  @override
  Future<Response> get(Uri url, {Map<String, String>? headers}) {
    return _client.get(url, headers: headers);
  }

  @override
  Future<Response> post(Uri url, {Map<String, String>? headers, Object? body, Encoding? encoding}) {
    return _client.post(url, headers: headers, body: body, encoding: encoding);
  }

  Map<String, String> _mergeHeader(Map<String, String>? headers){
    return {..._defaultHeader, ...?headers};
  }

  void setHeader(Map<String, String> headers){
    _defaultHeader = headers;
  }
  String printHeader(){
    return _defaultHeader.toString();
  }

}
