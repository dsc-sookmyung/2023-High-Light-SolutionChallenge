import 'package:flutter/material.dart';
import 'package:leturn/models/MClient.dart';

class AuthProvider extends ChangeNotifier{
  MClient client = MClient();

  void setClientHeader(Map<String, String> headers) {
    client.setHeader(headers);
  }
}