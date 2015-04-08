LOG
===

## Project Initialisations and Database Model+API

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

   ```python
	   >>> from polls.models import Question, Choice
	   >>> Question.objects.all()
	   >>> from django.utils import timezone
	   >>> q = Question(question_text="whats up?", pub_date=timezone.now())
	   >>> q.save()  #to save q in database
	   >>> q.id
	   >>> q.question_text
	   >>> q.pub_date
	   >>> Question.objects.all()
	   >>> q.was_published_recently()
	   >>> Question.objects.filter(id=1)
	   >>> Question.objects.get(pk=1) 	#pk=primary key
	   >>> Question.objects.filter(question_text__startswith='What')	#predefined database api function
	   >>> Question.objects.get(pub_date__year=timezone().now().year)
   ```

   Django creates a 'set' to hold the "other side" of a foreign key relation. Like in this case choices is a table which has a foreign key relation to questions. So django will have a set of all choices that belong to a particular question.

   ```python
   		>>> q = Question.objects.get(pk=1)
   		>>> q.choice_set.create(choice_text='nothing much', votes=0)
   		>>> q.choice_set.create(choice_text='lots of work', votes=0)
   		>>> c = q.choice_set.create(choice_text='dont know', votes=0)
   		>>> c.question 		# reverse relation
   		>>> q.choice_set.all()
   		>>> q.choice_set.count()
   ```

   Django's database API automatically follow the relationship to any depth as far as we need, no limit. Just need to use double underscores to saperate relationships.
   
   ```python
   		>>> # Find all Choices for any question whose pub_date is in this year
   		>>> Choice.objects.filter(question__pub_date__year=timezone.now().year)
   ```

   Delete any object-

   ```python
   		>>> c = q.choice_set.filter(choice_text__startswith='nothing')
   		>>> c.delete()
   ```

   Documentation :
   + [Accessing related objects](https://docs.djangoproject.com/en/1.8/ref/models/relations/)
   + [Double underscore field lookups](https://docs.djangoproject.com/en/1.8/topics/db/queries/#field-lookups-intro)
   + [Database API reference](https://docs.djangoproject.com/en/1.8/topics/db/queries/)

 - To display proper object representations like in `Question.objects.all()` or in django generated default admin panel, define __str__ function in python 3 and __unicode__ function in python 2.


##Django Site Admin's Panel

 - `python manage.py createsuperuser`

 - Run server and login.

 - To add questions from poll, edit `polls/admin.py`
 	```python
		from .models import Question
		admin.site.register(Question)
   ```

   To define the order of fields,
   ```python
		from .models import Question
		class QuestionAdmin(admin.ModelAdmin):
		    fields = ['pub_date', 'question_text']

		admin.site.register(Question, QuestionAdmin)
   ```

   To divide into fieldsets,
   ```python
   		from .models import Question
   		class QuestionAdmin(admin.ModelAdmin):
   			fieldsets = [
   			(None, {'fields': ['question_text']}),
   			('Date Information', {'fields': ['pub_date']}),
   		]

   		admin.site.register(Question, QuestionAdmin)
   ```

   To add collapse class to field so that initially it is shown hidden.
   ```python
   		#...
   		('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
   	```

   To add choice model inline with questions.
   ```python
   		class ChoiceInLine(admin.TabularInline):
   			model = Choice
   			extra = 3

   		# in class QuestionAdmin(admin.ModelAdmin):
   		# add
   		inlines = [ChoiceInline]
   ```
   To add searching facility, filter, and change the display of question :
   ```python
   		list_display = ('question_text', 'pub_date', 'was_published_recently')
    	list_filter = ['pub_date']
    	search_fields = ['question_text']
   ```

 - To modify the templates of admin panel like header or design,
 	+ `mkdir templates` [inside the project folder i.e. polling folder containing manage.py]
 	+ `cd templates`
 	+ `mkdir admin`
 	+ copy the templates from django's source code

 		`venv/lib/python2.7/site-packages/django/contrib/admin/templates/admin/base_site.html`
 		to `admin`
	+ modify the templates
	+ Edit `polling/settings.py`
	+ add `os.path.join(BASE_DIR,'templates')` in `DIRS` field in `TEMPLATES`

##Writing Views and Config URLs

 - __HttpResponse__
   ```python
   		from django.http import HttpResponse

   		def index(request):
   			return HttpResponse("Hello Someone")
   ```

 - First, add a view in `polls/views.py` using HttpResponse.
 - `touch urls.py` in `polls/`
 - polls/urls.py
   ```python
         from django.conf.urls import url
         from . import views

         urlpatterns = [
             url(r'^$', views.index, name='index'),
         ]
   ```
 - Add `url(r'^polls/', include('polls.urls')),` in urlpatterns in `polling/urls.py`
   [Notice that regular expression `r'^polls/` ends with trailing / without $, the ending symbol. This is because url continues after polls/ and the remaining part of url will be matched from polls/urls.py]

 - To pass additional arguements to views from the URL, we capture the values using regex.
   ```python
      # url : 34/ can be captured and question_id will be equal to 34
      url(r'^(?P<question_id>[0-9]+)$', views.details, name='details')
   ```
   Using parentheses around a pattern “captures” the text matched by that pattern and sends it as an argument to the view function.`?P<question_id>` is the name that will be used to identify the matched pattern and `[0-9]+` is the regular expression to match the sequence of digits.

   The view capturing this question_id will be
   ```python
         def details(request, question_id):
            return HttpResponse("You are at %s" % question_id)
   ```
 
 - Modifying templates for polls app
   ```
      cd polls
      mkdir templates
      cd templates
      mkdir polls
      cd polls
      touch index.html
   ```
   Note that the structure is
   ```
      polls/
         |- templates/
               |- polls/
                     |- index.html
   ```
   It is important to put index.html inside the folder __polls__ in __templates__. It can be referred to as `polls/index.html`. No need to change anything in `DIRS` field in `TEMPLATES` variable in `polling/settings.py`.

 - Methods :
   
   |      Function           |                Import                                     |
   |-------------------------|-----------------------------------------------------------|
   | __Loader__              | `from django.template import loader`                      |
   | __RequestContext__      | `from django.template import RequestContext`              |
   | __Render__              | `from django.shortcuts import render`                     |
   | __Http404__             | `from django.http import Http404`                         |
   | __get_object_or_404()__ | `from django.shortcuts import get_object_or_404`          |
   

 - To render and return template
   + `loader.get_template` for loading the template
   + `RequestContext` for creating context
   + `render` is the shortcut for these two steps which can be used
   + variables to the templates are passed using RequestContext

   ```python
         def index(request):
             latest_question_list = Question.objects.order_by('-pub_date')[:5]
             template = loader.get_template('polls/index.html')
             context = RequestContext(request, {
                 'latest_question_list': latest_question_list,
             })
             return HttpResponse(template.render(context))
   ```
 
 - Shortcut to render template
   
   ```python
      # def index(request) ....
      context = {'latest_question_list': latest_question_list}
      return render(request, 'polls/index.html', context)
   ```
 
 - Raising 404
   + 
     
     ```python
         # def details(request, question_id) ...
         try:
              question = Question.objects.get(pk=question_id)
         except Question.DoesNotExist:
              raise Http404("Question does not exist")
     ```
   + **get_object_or_404()** [similar function `get_list_or_404()`]
     
     ```python
         # def details(request, question_id) ...
         question = get_object_or_404(Question, pk=question_id)
         return render(request, 'polls/detail.html', {'question': question})
     ```

 - Removing Hardcoded urls

   ```html
      <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
   ```
   'detail' is the name given in `polls/urls.py` to the url defination/pattern.

   ```python
      url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
   ```

   'question.id' will come from the question object passed while rendering the template.

 - Using NameSpace

   When there are multiple apps and they all have detail view function, namespace is used to identify correct url.

   ```html
   <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
   ```

   For this, edit `polling/urls.py` and add namespace

   ```python
   url(r'^polls/', include('polls.urls', namespace="polls")),
   ```
 - You should always return an HttpResponseRedirect after successfully dealing with POST data.

##Templating

 - For loop
   
   ```
      {% for choice in question.choice_set.all %}
          <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
          <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
      {% endfor %}
   ```

 - Form

   ```
      <form action="{% url 'polls:vote' question.id %}" method="post">
         {% csrf_token %}
            ....
         <input type="submit" value="Vote" />
      </form>
   ```
