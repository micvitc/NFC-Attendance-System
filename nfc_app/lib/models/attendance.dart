class AttendanceModel {
  final String rfidSerialId;
  final String registerNo;
  final String name;
  final String content;
  bool markedAttendance;

  AttendanceModel({
    required this.rfidSerialId,
    required this.registerNo,
    required this.name,
    required this.content,
    this.markedAttendance = false,
  });

  factory AttendanceModel.fromJson(Map<String, dynamic> json) {
  return AttendanceModel(
    rfidSerialId: json['rfidSerialId'],
    registerNo: json['registerNo'],
    name: json['name'],
    content: json['content'],
  );
}
}
