from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Choice, Question


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
    p = get_object_or_404(Question.objects.get(pk=question_id))
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
                      'question': p,
                      'error_message': "You didn't select a choice"
                      })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args(p.id,)))
