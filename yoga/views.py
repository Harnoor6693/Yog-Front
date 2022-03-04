from django.shortcuts import render

def index(request):
    return render(request,'home.html')

def login(request):
    return render(request, 'login.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')

def blogs(request):
    return render(request, 'blogs.html')

def videos(request):
    return render(request, 'videos.html')

def catogery(request):
    return render(request, 'catogery.html')