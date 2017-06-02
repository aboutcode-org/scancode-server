# scancode-server


*An Overview :* 

Building a project which uses ScanCode as a library in a web and REST API application that allows you to scan code on demand by entering a URL and then store the scan results. Travis or Github integration to scan on commit with webhooks. Including the feature to scan based on a received tweet of similar IRC or IM integration.

### Installation

- Get the requirements

`$ sudo apt-get install python-pip`

`$ sudo pip install virtualenv`

- Create a virtual environment

	- `cd` into the directory where you want to install the virtual environment
  
  	`$ virtualenv .`
  
- Fork and clone the scancode-server repository

	`$ git clone https://github.com/your_username/scancode-server`

- Now get the django specific requirements 
 	
	`$ cd scancode-server`
  
  	`$ pip install requirements.txt`

- Now run the server 
 	
	`$ python manage.py runserver`

open [127.0.0.1:8000](127.0.0.1:8000) in the browser

### Database setup

- Create the database using these commands

	`$ mysql -u root -p`

- Enter your mysql password

- Create a database having a name of your choice. (Let's call it DATABASE_NAME)

	`> create database DATABASE_NAME;`

- Exit from the mysql
	
	`> exit;`

- Now add the information in the settings.py file

	`vim scancodeServer/settings.py`

- Find the dictionary DATABASES in the file and add the relevent information to it.

- Apply the migrations

	`python manage.py makemigrations`

	`python manage.py migrate`

- Create the admin

	`python manage.py createsuperuser`

- Add the relevant information

- open [127.0.0.1:8000/admin](127.0.0.1:8000/admin)
