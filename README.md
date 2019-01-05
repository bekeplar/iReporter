# iReporter

 iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention

[![Build Status](https://travis-ci.org/bekeplar/iReporter.svg?branch=develop)](https://travis-ci.org/bekeplar/iReporter)
[![Coverage Status](https://coveralls.io/repos/github/bekeplar/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/bekeplar/iReporter?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/af89820c26cf454cb407/maintainability)](https://codeclimate.com/github/bekeplar/iReporter/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e8dd68d2fd664a85a1bfca826127d6fd)](https://www.codacy.com/app/bekeplar/iReporter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bekeplar/iReporter&amp;utm_campaign=Badge_Grade)

## Required features

- Users can create an account and log in. 
- Users can create a ​red-flag ​​record (An incident linked to corruption). 
- Users can create ​intervention​​ record​ ​​(a call for a government agency to intervene e.g  repair bad road sections, collapsed bridges, flooding e.t.c). 
- Users can edit their ​red-flag ​​or ​intervention ​​records. 
- Users can delete their ​red-flag ​​or ​intervention ​​records.  
- Users can add geolocation (Lat Long Coordinates) to their ​red-flag ​​or ​intervention  records​. - - Users can change the geolocation (Lat Long Coordinates) attached to their ​red-flag ​​or  intervention ​​records​. 
- Admin can change the ​status​​ of a record to either ​under investigation, rejected ​​(in the  event of a false claim)​ ​​or​ resolved ​​(in the event that the claim has been investigated and  resolved)​. 


## Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v1/redflags|Create a redflag resource
GET|api/v1/redflags|Fetch all redflags reported
GET|api/v1/redflags/<red-flag-id>|Fetch a specific redflag record
DELETE|api/v1/redflags/<int:id>|Delete a specific redflag
PATCH|api/v1/redflags/<int:id>/location|Edit location of a specific redflag
PATCH|api/v1/redflags/<int:id>/comment|Edit a comment of a specific redflag
PATCH|api/v1/redflags/<int:id>/status|Edit status of a specific redflag
POST|api/v1/signup|create a new user
POST|api/vi/login|Login a user

## Requirements

- Python
- Flask
- Virtualenv
- Postman

## Getting started
* Clone the project to your local machine
```
git clone https://github.com/bekeplar/iReporter.git
```
* Change to the cloned directory
```
cd iReporter
pip install virtualenv
source venv/bin/activate
git checkout develop
pip install -r requirements.txt
python run.py
```
* For those on windows
```
cd iReporter
python -m venv venv
venv\Scripts\activate
```
* Run tests by
```
pip install pytest
pytest

```
* Testing Endpoints
```
copy the url in the terminal
paste it in postman
Use the following sample data
redflag = [
    {
        "createdBy":"Bekalaze",
        "type":"redflag",
        "title":"corruption",
        "location":"1.33, 2.045",
        "comment":"corrupt trffic officers in mukono",
        "status":"draft",
        "images":"nn.jpg",
        "videos":"nn.mp4"
    }
]

user = [
    {
        "firstname":"bekelaze",
        "lastname":"Joseph",
        "othernames":"beka",
        "email":"bekeplar@gmail.com",
        "phoneNumber":"0789057968",
        "username":"bekeplar",
        "isAdmin":"False",
        "password":"bekeplar1234"
    }
]
    
```
## Authors:
Bekalaze Joseph

### Courtesy of :
Andela Uganda
