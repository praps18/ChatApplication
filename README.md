# ChatApplication

Install following to make this project work

python
django
channels
daphne
pytest
selenium
FireFox driver
Execute the following commands in order

go to the root directory

python manage.py makemigrations group

python manage.py migrate group

python manage.py makemigrations

python manage.py migrate

#To create superuser(Admin)
python manage.py createsuperuser

#To run the project 
python manage.py runserver

Now open broswer and click on 

#this will gives you the home page
localhost:8000 


To run the test cases 
go to Tests Folder
cd Tests 
now run  pytest signintest.py

