from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("<a href='image-processing/docs'>DOCS</a>")
