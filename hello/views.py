from django.shortcuts import render,HttpResponse

# Create your views here.
def myview_(request):
    print(request.COOKIES)
    resp = HttpResponse(('hello developer here the string 8621cddd'))
    resp.set_cookie('dj4e_cookie', '8621cddd', max_age=1000)
    return resp

def myview(request):
    #counts how many have i visited the page
    num_visits = request.session.get('num_visits',0) + 1
    request.session['num_visits'] = num_visits
    resp = HttpResponse('view count='+ str(num_visits))

    #setting a cookie in key:value order
    resp.set_cookie('dj4e_cookie', '8621cddd', max_age=1000)

    return resp
