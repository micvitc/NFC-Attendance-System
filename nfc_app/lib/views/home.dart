import 'dart:async';
import 'package:flutter/material.dart';
import 'package:nfc_app/controllers/attendance_controller.dart';
import 'package:nfc_app/models/attendance.dart';

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final AttendanceController attendanceController = AttendanceController();
  String message = '';
  bool isMonitoring = false;

  void showMessage(String text) {
    setState(() {
      message = text;
    });

    Timer(const Duration(seconds: 2), () {
      setState(() {
        message = '';
      });
    });
  }

  void startMonitoring() async {
    setState(() {
      isMonitoring = true;
    });

    while (isMonitoring) {
      String rfidSerialId = await attendanceController.readNfcTag(context);
      List<AttendanceModel> attendanceList =
          await attendanceController.fetchAttendanceData();
      String attendanceMessage =
          attendanceController.markAttendance(rfidSerialId, attendanceList);
      showMessage(attendanceMessage);
    }
  }

  void stopMonitoring() {
    setState(() {
      isMonitoring = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('NFC Attendance System'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (message.isNotEmpty)
            Text(
              message,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
          const SizedBox(height: 20),
          Center(
            child: ElevatedButton(
              child:
                  Text(isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'),
              onPressed: () {
                if (isMonitoring) {
                  stopMonitoring();
                } else {
                  startMonitoring();
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}
