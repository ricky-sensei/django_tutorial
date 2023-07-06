from django.template import loader
from django.http import  HttpResponse
from .models import Question

def index(request):
    latest_question_list =  Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request, question_id):
    response = "質問 %s をみてるよ"
    return HttpResponse(response % question_id)

def result(request, question_id):
    response = "質問 %s の結果をみてるよ"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "質問 %s の投票結果をみてるよ"
    return HttpResponse(response % question_id)


