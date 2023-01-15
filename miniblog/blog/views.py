from django.shortcuts import render,HttpResponseRedirect
from.forms import signupform,loginform,postform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import post
from django.contrib.auth.models import Group,User

# Create your views here.

def home(request):
    posts=post.objects.all()
    return render (request,'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')
def contact(request):
    return render(request,'blog/contact.html')
def dashboard(request):
    if request.user.is_authenticated:
        posts=post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')


def signup(request):
    if request.method == 'POST':
        form=signupform(request.POST)
        if form.is_valid():
            messages.success(request,'!!!Successfully signup!!!')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
            login(request,user)
            return HttpResponseRedirect('/dashboard/')
            
    else:
        form=signupform()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form=loginform(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                pas=form.cleaned_data['password']
                user=authenticate(username=uname,password=pas)
                if user is not None:
                    login(request,user)
                    messages.success(request,'!!!Successfully login!!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=loginform()
    else:
        return HttpResponseRedirect("/dashboard")
    return render(request,'blog/login.html',{'form':form}) 

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def addpost(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=postform(request.POST)
            if form.is_valid():
                form.save()
                form=postform()
        else:
            form=postform()
        return render(request,'blog/add.html',{'form':form})
    else:
        return HttpResponseRedirect("/login/")

    
        

def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=post.objects.get(pk=id)
            form=postform(request.POST,instance=pi)
            if form.is_valid():
                form.save()          
        else:
            pi=post.objects.get(pk=id)
            form=postform(instance=pi)
        return render(request,'blog/update.html',{'form':form})
    else:
        return HttpResponseRedirect("/login/")

def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

