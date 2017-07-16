# scancode-server

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/59da2f264a5947209f05303cfbe8a223)](https://www.codacy.com/app/RajuKoushik/scancode-server?utm_source=github.com&utm_medium=referral&utm_content=nexB/scancode-server&utm_campaign=badger)


*An Overview :* 

Building a project which uses ScanCode as a library in a web and REST API application that allows you to scan code on demand by entering a URL and then store the scan results. Travis or Github integration to scan on commit with webhooks. Including the feature to scan based on a received tweet of similar IRC or IM integration.

### Installation (python 2.7)

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
  
  	`$ pip install -r requirements.txt`

- Now run the server 
 	
	`$ python manage.py runserver`

open [127.0.0.1:8000](127.0.0.1:8000) in the browser

### Database setup(postgresql)

- Install postgresql

	`$ sudo apt-get update`
	`$ sudo apt-get install postgresql postgresql-contrib`

- Start postgresql server
	
	`$ /etc/init.d/postgresql start`

- Start postgresql shell
	
	`$ sudo -i -u postgres`

- Create a user for scancode
	
	`$ createuser --interactive --pw`

	Now enter the relevant information. We don't want the user to be superuser. We do want the user to create database and we don't want the user to create roles

- Now create the database
	
	`$ create database DATABASE_NAME`

- Now open up the psql interactive shell
	
	`$ psql`

- Grant all privileges to the newly created user
	
	`# grant all privileges on database DATABASE_NAME to USER_NAME;`

- Quit the interactivee shell
	
	`# \q`

- Exit from postgresql shell
	
	`$ exit`

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
