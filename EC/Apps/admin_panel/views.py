from django.shortcuts import render, HttpResponse

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard.html')

def post_list(request):
    return render(request, 'post-list.html')

def riddles(request):
    return render(request, 'post-list.html')

def share_sth_interesting(request):
    return render(request, 'post-list.html')

def find_friends(request):
    return render(request, 'post-list.html')

def ask_for_help(request):
    return render(request, 'post-list.html')

def else_list(request):
    return render(request, 'post-list.html')