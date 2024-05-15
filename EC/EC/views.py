from django.shortcuts import render, HttpResponse


def index(reqeust):
    return render(reqeust, 'index.html')