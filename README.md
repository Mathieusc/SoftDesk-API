# Openclassrooms Project 10
Create a secured RESTful API using Django REST framework

## SoftDesk API

API made to track issues for multiple platforms (iOS, ANDROID, WEB) and assign users to them.
All endpoints are explained in the documentation below.

## SoftDesk Documentation

https://documenter.getpostman.com/view/19912950/Uyr7HyZP


Main features :
- User Authentication (using JWT)
- Create projects
- Create issues for a project
- Create comments for an issue
- Add contributors
- Update/Delete methods with permissions

## Installation

Python (version 3.8.10)
* [Download Python](https://www.python.org/downloads/) 

Download the application
```
git clone https://github.com/Mathieusc/openclassrooms_project_10.git
```

Create a virutal environment
```
python -m venv env
```

Linux :
```
source env/bin/activate
```

Windows :
```
.\env\Scripts\Activate
```

Install dependencies
```
pip install -r requirements.txt
```

Create the database
```
python manage.py makemigrations
python manage.py migrate
```

Create the admin account
```
python manage.py createsuperuser
```


## Created with
Python version 3.8.10
* [Visual Studio Code](https://code.visualstudio.com/) 
* [Postman](https://www.postman.com/)
