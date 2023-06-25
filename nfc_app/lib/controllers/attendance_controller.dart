import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:nfc_app/models/attendance.dart';
import 'package:nfc_manager/nfc_manager.dart';
import 'package:http/http.dart' as http;

class AttendanceController {
  Future<List<AttendanceModel>> fetchAttendanceData() async {
    var response =
        await http.get(Uri.parse('https://navi2329.github.io/attendance.json'));
    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      List<AttendanceModel> attendanceList =
          data.map((item) => AttendanceModel.fromJson(item)).toList();
      return attendanceList;
    } else {
      throw Exception('Failed to load attendance data');
    }
  }

  Future<String> readNfcTag(BuildContext context) async {
    Completer<String> completer = Completer<String>();
    try {
      await NfcManager.instance.startSession(
        onDiscovered: (NfcTag tag) async {
          if (tag.data['nfca'] != null &&
              tag.data['nfca']['identifier'] != null) {
            List<int> identifier = tag.data['nfca']['identifier'];
            String rfidSerialId = identifier
                .map((byte) => byte.toRadixString(16).padLeft(2, '0'))
                .join(':');
            completer.complete(rfidSerialId);
            await NfcManager.instance.stopSession();
          }
        },
      );
    } catch (e) {
      completer.completeError(e);
    }

    return completer.future;
  }

  String markAttendance(
      String rfidSerialId, List<AttendanceModel> attendanceList) {
    for (AttendanceModel attendance in attendanceList) {
      if (attendance.rfidSerialId == rfidSerialId) {
        attendance.markedAttendance = true;
        return 'Attendance marked for ${attendance.name}';
      }
    }
    return 'No matching student found';
  }
}
