from django.urls import path
from . import views

urlpatterns = [
	path('login', views.login, name ='login'),
	path('logout',views.logout ,name='logout'),
	path('show', views.PhotoList.as_view()),
	path('signup', views.signup, name='signup'),
	path('new/',views.photo_new, name = 'photo_new'),
    path('', views.index, name='index'),
]

