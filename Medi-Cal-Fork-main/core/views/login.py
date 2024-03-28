from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from medical import settings
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from ..login.tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# Create your views here.
class default(TemplateView):
    template_name = 'index.html'

class signup(TemplateView):
    template_name = "signup.html"
    def post(self, request):
        if request.method == "POST":
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if User.objects.filter(username=username):
                messages.error(request, "Username already exists.")
                self.template_name = "index.html"
                return render(request, self.template_name)
            
            if User.objects.filter(email=email):
                messages.error(request, "Email already registered.")
                self.template_name = "index.html"
                return render(request, self.template_name)
            
            if len(username)>15:
                messages.error(request, "Username must be under 15 characters.")

            if pass1 != pass2:
                messages.error(request, "Passwords do not match.")

            if not username.isalnum():
                messages.error(request, "Username must be alpha-numeric.")
                self.template_name = "index.html"
                return render(request, self.template_name)


            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()

            messages.success(request, "Your account has been successfully created. A confirmation email has been sent. Please confirm your email in order to activate your account.")

            
            #Welcome Email
            subject = "Welcome to Medi-Cal!"
            message = "Hello " + myuser.first_name + "! \n" + "Welcome to Medi-Cal! \nThank you for visiting our website. \nWe have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\nThank you."
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your email."
            message2 = render_to_string('email_confirmation.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            self.template_name = "signin.html"
            return render(request, self.template_name)

        return render(request, self.template_name)

class signin(TemplateView):
    template_name = 'signin.html'
    def post(self, request):

        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass1']

            user = authenticate(username=username, password=pass1)

            if user is not None:
                login(request, user)
                fname = user.first_name
                return render(request, "index.html", {'fname': fname})

            else:
                messages.error(request, "Wrong Credentials.")
                self.template_name = "index.html"
                return render(request, self.template_name)
            
        return render(request, self.template_name)

class signout(TemplateView):
    template_name = 'home.html'
    def post(self, request):
        logout(request)
        messages.success(request, "Logged Out Successfully.")
        self.template_name = "index.html"
        return render(request, self.template_name)

class activate(TemplateView):
    template_name = 'activationfailed.html'
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
        
        if myuser is not None and generate_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            login(request, myuser)
            self.template_name = "index.html"
            return render(request, self.template_name)
        else:
            return render(request, self.template_name)