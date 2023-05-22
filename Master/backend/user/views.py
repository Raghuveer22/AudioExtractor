from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm
from base.forms import SongUploadForm
from base.models import Audio
from django.contrib.auth import logout
from base.utils import Youtube,Video
import datetime
from django.core.files import File as DjangoFile
def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST,request.FILES)
        if form.is_valid():
            if 'url' in form.cleaned_data:
                url = form.cleaned_data['url']
                print(url)
                _obj=Youtube(url)
                _obj.youtube_to_mp3()
                name= _obj.name
                file_name=_obj.rand
                video_length=datetime.timedelta(seconds=_obj.length) 
                f=open(_obj.file_path,"rb")
                audio=Audio(upload_file = DjangoFile(f,name=str(file_name)+".mp3"),duration=video_length,name=name,uploaded_by=request.user)
                audio.save()
            elif 'file' in form.cleaned_data:
                file = request.FILES
                _obj=Video(file)
                _obj.video_to_mp3()
                name= _obj.name
                file_name=_obj.rand
                video_length=datetime.timedelta(seconds=_obj.length)
                f=open(_obj.out_file,"rb")
                audio=Audio(upload_file = DjangoFile(f,name=str(file_name)+".mp3"),duration=video_length,name=name,uploaded_by=request.user)
                audio.save()
    else:
        form=SongUploadForm()
    return render(request, 'home.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home') 
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})
