# Group 5 Understudyathon: Essay Grader

A platform to speed up essay grading.

## Setup


All necessary libraries can be installed using the following command: 
```
pip3 install -r requirements.txt
```

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
	- [ ] Grammar
	- [ ] Citation Formatting
	- [ ] Citation Cross-Referencing
	- [ ] Header Formatting
	- [ ] Plagarism Checker
* Interface:
	* Teacher 
		- [ ] Seeing Students Essay's and being able to grade it
		- [ ] Comment System(Interact with Students)
	* Student
		- [ ] Submitting Essay and Seeing Errors
		- [ ] Seeing Students Essay's and being able to grade it
		- [ ] Comment System(Interact with Students)
* Frameworks:
	* Django
	* Bootstrap
	* HTML/CSS/JavaScript
* OAuth2:
	- [ ] Setting up Ion OAuth
	- [ ] OAuth2 Library to verify if user is a student or a teacher
	* Using Ion to Login


## Program Structure
* Front-End and Back-End Structure
