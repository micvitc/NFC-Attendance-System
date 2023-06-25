import 'package:flutter/material.dart';
import 'package:nfc_app/views/home.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NFC Attendance System',
      home: Home(),
    );
  }
}
