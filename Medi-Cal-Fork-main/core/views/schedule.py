from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from ..models import Surgeon
# Create your views here.
# view function: request -> response (request handler)
class masterschedule(TemplateView):
    template_name = 'masterschedule.html'
    def post(self, request):
        '''
        Testing View Function that is called at an url
        '''
        dict = {}
        Surgeons = [Surgeon(fullName = "John Smith", assignments = [], availability = [], exp = "Sr", qualifications = [])] #list of surgeon objects to be linked with database
        dict["surgeons"] = Surgeons
        return render(request, self.template_name, dict)

class appointment(TemplateView):
    template_name = 'personschedule.html'
    def post(self, request):
        '''
        Website to add scheduling stuff
        '''
        dict = {}
        surgeonlst = [Surgeon("John Doe", ["www"], ["www"], "Sr", ["www"]), Surgeon(fullName = "John Smith", assignments = [], availability = [], exp = "Sr", qualifications = [])] #list of surgeon objects to be linked with database
        dict["surgeons"] = surgeonlst
        return render(request, self.template_name, dict)

class personschedule(TemplateView):
    template_name = 'personschedule.html'
    def post(self, request):
        return render(request, self.template_name, {})

class index(TemplateView):
    template_name = 'index.html'
    def post(self, request):
        '''
        View function displays calls template to display current surgeons
        Input:
            request (HTML request)
        Output:
            render() (HTML file): note 
        '''
        return render(request, self.template_name,{})


"""
#login page at /schedule/login
def login(request):
    return HttpResponse('<h1> This is a login page </h1>')

#signup page at /schedule/signup
def signup(request):
    return HttpResponse('<h1> This is a signup page </h1>')
"""