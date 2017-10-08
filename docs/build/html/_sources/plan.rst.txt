Common Plan
===========================================


#### Goals

1. Create a backend server in Django to run ScanCode.
2. Add helpful features to ScanCode server and implement storage.
3. Create GitHub integration feature on the server.
4. Create a nice website for the project.
5. Write the basic documentation.
6. Create the Twitter bot to scan code and return the result.
7. Create the Slack bot to scan code and return the result.

The starred goals could be carried out if there are no time constraints.

#### Goal 1: Create a backend server in Django to run ScanCode.

##### SUBTASKS

- [X] Initialize the Django project.
- [X] Setup Django Rest Framework for the API.
- [X] Put all the requirements in the requirements.txt file.
- [X] Writing the getting started documentation.
- [X] Allow uploading from the local.
- [X] Allow scanning of URL’s.
- [X] Run the scancode commands on the server.
- [X] POST API would be scripted to scan the code and which would return the HTML or JSON giving the results as a response to the POST request.


#### Goal 2: Add helpful features to ScanCode server and implement storage.
##### The following models are needed to be implemented.
- [X] User model - Already exists. We only need to use it.
- [X] User history model
- [X] The code information model
- [X] Scanned results

##### SUBTASKS
- [ ] Create POST API endpoint to ScanCode given GitHub or BitBucket or Git URL.
- [X] Use Celery in the backend.
- [X] Show the status of the scan while the scanning is going on and scan result when the scan is complete.
- [] The scanning can take a lot of time depending on the size of the project so I suggest we should use a Celery queue in the background and let the scan run there. Once the scan is done, we can return the result URL in the API response.
What celery does here is, once an API request to send a GitHub repo is sent, we will queue the task of scanning that repo in Celery. Then we will return the user with a task URL. The user will have to periodically send a GET request to the task_url to see if the job is finished. Once the job is finished, the response at task_url will change and it will show the URL to fetch scan result.

##### Note:

At this point, we have two types of return for an API request to scan code. We should go with the Celery based approach because we can’t be sure that ScanCode will always finish in a fraction of second. And stalling the server’s main thread is never a good idea. So the response type of scan requests should be Celery based task_url.

#### Goal 2.5 Write unit tests
- [X] Write unit tests for tasks.py
- [X] Write unit tests for views.py
- [X] Write unit tests for models.py

#### Goal 3: Create GitHub integration feature on the server.

GitHub integration can be a cool feature for ScanCode. Using this, people would be able to hook ScanCode in their repos and each time they do a commit or a PR, our server will send a comment in the commit/PR telling what new licenses were added and what were deleted.

##### SUBTASKS

- [ ] Create API endpoint to check for commit (single) changes.
- [ ] Create API endpoint to check for PR (can be multiple commits) changes.
- [ ] Create a Travis script (in Python) to send a request to those endpoints with the commit/PR information.
- [ ] This script will also wait for and fetch the response and send it as a comment to the respective commit/PR.
- [ ] Implement a webhook in the server to do the same. It will also receive commit/PR information as API actions and it will analyze the commit/PR and post back comments on GitHub with the ScanCode report.

#### Goal 4: Website

After the features of this project are completed, I plan to create a nice website to show information about using the ScanCode API, the GitHub integration and the Twitter and Slack bots. This website will just contain few beautiful pages with information on these topics.

##### SUBTASKS

- [X] Create the website using Django.
- [ ] Host it on AWS or any other hosting service.


The following page can be the home page of the scancode website. The main components to the homepage are:

#### First View:
![home](https://cloud.githubusercontent.com/assets/11356398/26746455/326730c0-480d-11e7-9219-da9334b427ac.png)
##### Header:

The homepage starts with a fixed header. On left, there is space for the logo or the name of the website. On the right corner we get the options to LOGIN and SIGNUP.

##### A quote:

A quote that describes what we are trying to achieve using this website.

##### Buttons:

These buttons are the main action buttons for the user. For now, we can add three options and later on we can add another option for the user who can choose a list. The three main options, for now, can be:

- [ ] Scan from a URL.
- [ ] Upload files from the PC.
- [ ] Write your code.

There is a separate line of action when the user chooses a different option.

##### Footer:

The page ends with a footer which will contain the copyright notice and the name of the parent company along with some reference to the important information.

#### Second view:
![second](https://cloud.githubusercontent.com/assets/11356398/26746456/326845dc-480d-11e7-8000-98d2930f4503.png)
Now this page will be opened if the user clicks on the scan an URL button. Most of the part will remain same. The only change that will come is in the centre where there will be an input box and label on the left saying: Enter the URL. Finally, there is an option to submit the code.

#### Third view:
![upload](https://cloud.githubusercontent.com/assets/11356398/26746454/3266f182-480d-11e7-910a-54d6742b59ed.png)
This page will be opened when the user clicks on the button saying UPLOAD files from local. Once the user selects the directories and clicks on the submit button, a progress bar will start and files will start uploading to the server.

For the third part, we will add a text editor where the user can enter or paste the code. When the user submits the code, we can add a feature to represent the different part of the code with different colours is a good option. We can represent the author and licence information with some different colours that differentiate it from the other part of the code.

#### Goal 5: Creating documentation

In this part, we will be working on making the documentation. How to install and how to use documentation is the least we can do for the start.



