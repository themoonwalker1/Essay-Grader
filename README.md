# Group 5 Understudyathon: Essay Grader

A platform to speed up essay grading.

## Setup

* Go to a suitable directory and clone the repository with
	* ```
  	  git clone git@github.com:TheMoonWalker1/Essay-Grader.git
  	  ```
* Next setup a virtual environment with the virtualenv library(Install it with for)
	* MacOs/Linux
		* ```
		  python3 -m pip install --user virtual env
		  ```
	* Windows
		* ```
		  py -m pip install --user virtualenv
		  ```
* Go to the directory where you cloned the repository and type
	* MacOs/Linux
		* ```
		  python3 -m venv venv
		  ```
	* Windows
		* ```
		  py -m venv venv
		  ```
* Next, you have to activate the virtual environment with
	* MacOs/Linux
		* ```
		  source venv/bin/activate
		  ```
	* Windows
		* ```
		  .\venv\Scripts\activate
		  ```
* Next, install all necessary libraries with the following command:
	* ```
	  pip3 install -r requirements.txt
	  ```
* Now run:
	* ```
	  python manage.py runserver
	  ```
	* And now go to http://127.0.0.1:8000/ to get access!
* Login using the Ion OAuth
* Note requires Python 3.6+

## Goals
* Essay Checking 
	- [x] Grammar
	- [x] Formatting
	- [ ] Citation Formatting
	- [ ] Citation Cross-Referencing
	- [ ] Header Formatting
	- [ ] Plagarism Checker
* Interface:
	* Teacher 
		- [x] Seeing Students Essay's and being able to grade it
		- [ ] Comment System(Interact with Students)
	* Student
		- [x] Submitting Essay
* Automation
	- [x] Adding Celery Works for Automation
* Frameworks:
	* Django
	* Bootstrap
	* HTML/CSS/JavaScript
* OAuth2:
	- [x] Setting up Ion OAuth
	- [x] OAuth2 Library to verify if user is a student or a teacher
	- [x] Adding RBAC(Role Based Access Control)

## Program Structure
* Front-End and Back-End Structure
* Teacher
	* Create Superuser
	* Front End
	* Back End
* Student
	* Front End
	* Back End
	* Login using Ion OAuth