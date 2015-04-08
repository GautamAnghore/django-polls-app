from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question Does Not EXIST")

    return render(request, 'polls/details.html', {'question': question})


def result(request, question_id):
    return HttpResponse("Polls result question : %s " % question_id)


def vote(request, question_id):
    return HttpResponse("votes for question : %s " % question_id)
