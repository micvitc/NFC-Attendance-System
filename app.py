from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask import Flask, request
from enum import Enum  
from datetime import datetime

class StatusEnum(Enum):
    absent = 'absent'
    present = 'present'


app= Flask(__name__)
marsh = Marshmallow(app)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nfc.sqlite3' 
db = SQLAlchemy(app) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(1000),nullable = False)
    nfc_serial = db.Column(db.String(100),unique = True, nullable = False)
    roll_no = db.Column(db.String(1000),nullable = False)
    faculty_registered = db.Column(db.String(1000),nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(1000),nullable = False)
    created_at = db.Column(db.DateTime)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.absent, nullable=False)
    date = db.Column(db.DateTime)
    meeting = db.relationship('Meeting', backref=db.backref('attendances', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('attendances', lazy='dynamic'))

class UserSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'nfc_serial', 'roll_no', 'faculty_registered', 'created_at', 'admin')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class MeetingSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'name', 'created_at')

meeting_schema = MeetingSchema()
meetings_schema = MeetingSchema(many=True)


class AttendanceSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'meeting_id', 'user_id', 'status', 'date')

attendance_schema = AttendanceSchema()
attendances_schema = AttendanceSchema(many=True)

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Get a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return user_schema.jsonify(user)


# Create a new user
@app.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    nfc_serial = request.json['nfc_serial']
    roll_no = request.json['roll_no']
    faculty_registered = request.json['faculty_registered']

    new_user = User(username=username, email=email, nfc_serial=nfc_serial, roll_no=roll_no, faculty_registered=faculty_registered)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


# Get all meetings
@app.route('/meetings', methods=['GET'])
def get_meetings():
    all_meetings = Meeting.query.all()
    result = meetings_schema.dump(all_meetings)
    return jsonify(result)


# Get a specific meeting
@app.route('/meetings/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    meeting = Meeting.query.get(meeting_id)
    return meeting_schema.jsonify(meeting)


# Create a new meeting
@app.route('/meetings', methods=['POST'])
def add_meeting():
    name = request.json['name']

    new_meeting = Meeting(name=name)
    db.session.add(new_meeting)
    db.session.commit()
    return meeting_schema.jsonify(new_meeting)


# Get all attendances
@app.route('/attendances', methods=['GET'])
def get_attendances():
    all_attendances = Attendance.query.all()
    result = attendances_schema.dump(all_attendances)
    return jsonify(result)


# Get attendance for a specific meeting
@app.route('/attendances/meetings/<int:meeting_id>', methods=['GET'])
def get_attendance_by_meeting(meeting_id):
    attendance = Attendance.query.filter_by(meeting_id=meeting_id).all()
    return attendances_schema.jsonify(attendance)


# Get attendance for a specific user
@app.route('/attendances/users/<int:user_id>', methods=['GET'])
def get_attendance_by_user(user_id):
    attendance = Attendance.query.filter



if __name__ == '__main__':
    app.run() 
    db.create_all()

