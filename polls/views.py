from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import  HttpResponse
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # ショートカットを利用
    context = {'latest_question_list':latest_question_list}
    return render(request, "polls/index.html")
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})

def result(request, question_id):
    response = "質問 %s の結果をみてるよ"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "質問 %s の投票結果をみてるよ"
    return HttpResponse(response % question_id)


