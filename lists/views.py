from django.shortcuts import render
#from django.http import HttpResponse
# Create your views here.
	#def home_page():
	#	return HttpResponse()
#def home_page(request):8/
	#return HttpResponse('<html>')
#def home_page(request):
	#return HttpResponse('<html><title>To-Do lists</title>')
#def home_page(request):
#	return HttpResponse('<html><title>To-Do lists</title></html>')
def home_page(request):
	return render(request,'home.html')
