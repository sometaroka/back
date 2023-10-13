from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse

def index(request):
    return render(request, "sometaroka/index.html")
    #return HttpResponse("Hello, world. You're at the polls index.")

def room(request, room_name):
    return render(request, "sometaroka/room.html", {"room_name": room_name})