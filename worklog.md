LOG
===

 - `django-admin startproject polls`
 - **settings :** database setting (engine : django.db.backends.mysql, name : dbname, host : localhost, user, password, port : 3306), `TIMEZONE : 'Asia/Kolkata'`
 - `python manage.py migrate`
 - **error :** no module named mysqldb
       **solution :** `pip install MySQL-python` 
 - `python manage.py runserver` | `python manage.py runserver 8080` | `python manage.py runserver 0.0.0.0:5000`
 - Inside `django-polls-app/polling` -> `python manage.py startapp polls`
 - Edit `polls/models.py`, define table properties
 - Edit `polling/settings.py`, add in `INSTALLED_APPS` value `'polls',`
 - `python manage.py makemigrations polls`
    This will create the database tables.
    + **error :** makemigrations command not found. **solution :** check if you are using right version, might be the case that the virtual env is not activated
 - 
