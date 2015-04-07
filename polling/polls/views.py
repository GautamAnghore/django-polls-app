from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))


def details(request, question_id):
    return HttpResponse("QuestionDetails : %s" % question_id)


def result(request, question_id):
    return HttpResponse("Polls result question : %s " % question_id)


def vote(request, question_id):
    return HttpResponse("votes for question : %s " % question_id)
