`                                 `MIC PROJECT: NFC BASED ATTENDANCE SYSTEM 


Description: 

`  `Developing an app to track attendance using the NFC tag present in student ID cards.  Creating API end points to successfully update the attendance based on the unique serial ID generated for each ID-card. 

Tentative schema: 



Tech requirements:   

- NFC scanning app

Web Dev:

- Poetry ( Virtual Environment Manager)
- Flask
- Flask-RESTful
- SQLAlchemy
- Flask- Marshmallow 
- React-Native

App Dev:

- Flutter 
- Flutter- NFC
- Http
- get

Workflow: 

- Two tables, one for user and the other for attendance are created. The serial number acts as the primary key
- On tapping the NFC using the app, a unique serial ID for each ID card is generated, this serial ID is used to populate the database along with other details of the students.
- After creating the database, on tapping, the  API endpoints are called and the database is queried based on the serial ID and the attendance table is updated.

