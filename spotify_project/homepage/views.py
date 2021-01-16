from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
	# return render(request, "homepage/home.html")
	# for now I am using HttpResponse, but as we build this out we should probably render the page from templates
	return HttpResponse('<h1>Welcome to our project</h1>')