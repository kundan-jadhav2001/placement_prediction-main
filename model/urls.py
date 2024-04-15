from django.urls import path
from model import views

urlpatterns = [
    path('',views.home),
    path('signinup',views.signinup),
    path('contact',views.contact),
    path('course',views.course),
    path('blog',views.blog),
    path('about',views.about),
    path('confirmsignup',views.confirmsignup),
    path('confirmsignin',views.confirmsignin),
    path('predictionpage', views.predictionpage),
    path('predict', views.predict),
    path('report', views.report),
    path('front', views.front),
    path('test', views.test),
    path('feedback', views.feedback),
    path('EXPLORE NOW', views.contact),
    path('savereview',views.savereview),
    path('logout',views.logout),
    
    path('forgotpass',views.forgotpass),
    path('setnewpass',views.setnewpass),
]
