LOG
===

 - `django-admin startproject polls`
 - **settings :** database setting (engine : django.db.backends.mysql, name : dbname, host : localhost, user, password, port : 3306), `TIMEZONE : 'Asia/Kolkata'`
 - `python manage.py migrate`
 - **error :** no module named mysqldb
       **solution :** `pip install MySQL-python` 
 - `python manage.py runserver` | 