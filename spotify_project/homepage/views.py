from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
	return render(request, "homepage/index.html")
	# fose, but as we build this out we should probably render the pr now I am using HttpResponage from templates
	# return HttpResponse('<h1>Welcome to our project</h1>')

# api calling functions go here: