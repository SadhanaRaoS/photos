from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login 
from django.contrib.auth import  authenticate
from .models import Photo
from .forms import AddPhotoForm
import logging
logger = logging.getLogger(__name__)


# Create your views here.

def signup(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			# user = authenticate(username=username, password=password)
			auth_login(request,user,backend='django.contrib.auth.backends.ModelBackend')
			request.session['user_id']= user.id
			response = render(request, 'show.html')
			respone.set_cookie(key ='id', value='1')
			return response
	else:
		form = UserCreationForm()
	return render(request, 'signup.html', {'form': form})

def login(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		logger.debug('Printing user',user)
		if user is not None:
			auth_login(request,user)
			return redirect('show')
		else:
			form = AuthenticationForm()	
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})

def logout(request):
	del request.session['user_id']

def photo_new(request):
	if request.method=='POST':
		form = AddPhotoForm(request.POST,request.FILES)
		if form.is_valid():
			photo = form.save(commit=False)
			photo.user = request.user
			photo.updated_at = timezone.now()
			photo.save()
		return render(request, 'photos/show.html')
	else:
		form = AddPhotoForm()
		return render(request,'photos/add_photo.html', {'form': form})

class PhotoList(generic.ListView):
	def get(self,request):
		if request.user.is_authenticated:
			logger.info('user obj is', request.user)
			context_object_name = 'photo_list'
			queryset = Photo.objects.filter(user=request.user).order_by('-updated_at')
		template_name = 'photos/show.html'
		if queryset:
			return render(request,self.template_name)
		else:
			form = AddPhotoForm()
			return render(request, 'add_photo.html', {'form': form})


def index(request):
	return HttpResponse("Hello World, You're at photos index")
