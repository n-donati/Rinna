from django.shortcuts import render

@csrf_protect
def home(request):
    return render(request, 'home.html')