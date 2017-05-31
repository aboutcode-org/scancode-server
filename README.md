# scancode-server


*An Overview :* 

Building a project which uses ScanCode as a library in a web and REST API application that allows you to scan code on demand by entering a URL and then store the scan results. Travis or Github integration to scan on commit with webhooks. Including the feature to scan based on a received tweet of similar IRC or IM integration.

### Installation

- Get the requirements

`sudo apt-get install python-pip`

`sudo pip install virtualenv`

- Create a virtual environment

	- `cd` into the directory where you want to install the virtual environment
  
  	`$ virtualenv .`
  
- Fork and clone the scancode-server repository

	`$ git clone https://github.com/your_username/scancode-server`

- Now get the django specific requirements 
 	
	`$ cd scancode-server`
  
  	`$ pip install Requirements.txt`

- Now run the server 
 	
	`$ python manage.py runserver`
