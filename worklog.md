LOG
===

 - `django-admin startproject polls`
 
 - **settings :** database setting (engine : django.db.backends.mysql, name : dbname, host : localhost, user, password, port : 3306), `TIMEZONE : 'Asia/Kolkata'`
 
 - `python manage.py migrate`
 
 - **error :** no module named mysqldb
       **solution :** `pip install MySQL-python` 
 
 - `python manage.py runserver`

   `python manage.py runserver 8080`

   `python manage.py runserver 0.0.0.0:5000`
 
 - Inside `django-polls-app/polling` -> 

   `python manage.py startapp polls`
 
 - Edit `polls/models.py`, define table properties
 
 - Edit `polling/settings.py`, add in `INSTALLED_APPS` value `'polls',`
 
 - `python manage.py makemigrations polls`
    
    This will tell django that some changes are made in database models. Will create a migration i.e. changes will be saved in form of migration which can be transformed into sql queries to affect the database. 
    + **error :** makemigrations command not found. **solution :** check if you are using right version, might be the case that the virtual env is not activated
 
 - To check the sql queries this migrate will execute : 

   `python manage.py sqlmigrate polls 0001`

   0001 is the name of migration file (0001_initial.py).

   Actual execution of commands do not take place using this command.

 - To check if there is any problem before making any actual migrations : 

   `python manage.py check`

 - To make actual migrations(i.e. executing the sql commands to make the changes to database) : 

   `python manage.py migrate`

 - To run the interactive shell with all the dependencies installed

   `python manage.py shell`

   ```
   >>>from polls.models import Question, Choice
   >>>Question.objects.all()
   >>>from django.utils import timezone
   >>>q = Question(question_text="whats up?", pub_date=timezone.now())
   >>>q.save() //to save q in database
   >>>q.id
   >>>q.question_text
   >>>q.pub_date
   >>>Question.objects.all()
   ```

 - To display proper object representations like in `Question.objects.all()`, define __str__ function in python 3 and __unicode__ function in python 2.

 - 
