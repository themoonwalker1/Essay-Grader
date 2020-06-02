# Group 5 Understudyathon: Essay Grader

A platform to speed up essay grading.

## Setup

 * Install RabbitMQ and Erlang
	* MacOS/Linux
		* Follow the instructions at https://www.rabbitmq.com/download.html
	* Windows
		* Issues during setup? Try going here:
			* https://www.rabbitmq.com/windows-quirks.html
		* For windows, it's easiest if you download RabbitMQ via Chocolatey. You can download Chocolatey here:
			* https://chocolatey.org/docs/installation
		* After you've installed chocolatey and made sure to add it to the PATH, make sure you're in a terminal which has administrative access and run 
			```
			choco install rabbitmq
			```
		* In a separate terminal window, go to the install location (such as C:\Program Files\RabbitMQ Server\rabbitmq_server-3.8.4) and add the sbin folder to the PATH. After this, run 
			```
			rabbitmq-server
			```
			* **Don't exit out of this terminal or stop this process when running any future commands. Instead, open up a separate terminal window and execute those tasks from there.** Stopping this process will kill the server, so you will have to start it again before running the Django app.
			* Note: since this command starts the server, you should see a picture of a rabbit in an ASCII-art format (this is RabbitMQ's logo), followed by some text, and finally a line which says "Starting broker"; no loading bars or anything special will pop up.

* Go to a suitable directory and clone the repository with
	* ```
  	  git clone git@github.com:TheMoonWalker1/Essay-Grader.git
  	  ```
* Move into the folder where the repository was cloned
	* ```
	  cd Essay-Grader
	  ```

* Next setup a virtual environment with the virtualenv library(Install it with for)
	* MacOs/Linux
		* ```
		  python3 -m pip install --user virtualenv
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
	* MacOS/Linux
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
	  python manage.py migrate
	  python manage.py runserver
	  ```
	* And now go to http://127.0.0.1:8000/ to get access!
* Login via Ion
* Note: requires Python 3.6+

## Goals
* Bold == Working On
* Website Features
	- [ ] ***Settings***
		- [ ] Add Teacher
		- [ ] Password Change
		- [ ] Add Login/Logout to the Sidebar(Maybe idk)
* Essay Checking 
	- [x] Grammar
	- [x] Formatting
	- [ ] ***Citation Formatting***
	- [ ] ***Citation Cross-Referencing***
	- [x] Header Formatting
	- [ ] Plagarism Checker
* Interface:
	* Teacher 
		- [x] Seeing Students Essay's and being able to grade it
		- [ ] Comment System(Interact with Students)
	* Student
		- [x] Submitting Essay
* Automation
	- [x] Adding Celery Works for Automation
	- [x] ***Finishing Optimization of Celery Algorithm***
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
