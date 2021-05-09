from django.shortcuts import render,HttpResponse,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from .models import Question,Choice




# Create your views here.
def owner(request):

    return HttpResponse("Hello, world. 9313f5e9 is the polls index.and 8621cddd")

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def result(request,id_):
     question = get_object_or_404(Question,id=id_)

     return render(request, 'polls/results.html',{'question':question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
 
    
def vote(request, id_):
    question = get_object_or_404(Question, pk=id_)
    k = Choice()
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def fuckoff(request):
    obj = get_object_or_404(Question,id=3)
    content ={
        'obj':obj
    }
    return render(request,'polls/chuck.html',content)

