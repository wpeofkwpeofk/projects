from django.urls import path #importing the path functions
from ..views import schedule #import view functions from current folder

#url configuration
urlpatterns = [
    path('', schedule.masterschedule, name='test'),
    path('test/', schedule.index, name='index'), #url path objects that receives the url, calls the function
    # path('login/', views.login, name='schedule-login'),
    # path('signup/', views.signup, name='schedule-signup')
    path('appointment/', schedule.appointment, name='appointment'),
    path('personschedule/', schedule.personschedule, name='personschedule')
]
