from django.contrib.auth.models import User
from django.shortcuts import render
from users_app.forms import UserForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views.generic import UpdateView
import secrets
from random import randint

def generate_account(request):
    flag=False

    while flag==False:
        temp_name=str(randint(100000000,999999999))
        if len(User.objects.filter(username=temp_name))==0:
            flag=True

    temp_password='0000'
    user = User.objects.create_user(username=temp_name,
                                 password=temp_password)
    user=authenticate(
                        username=temp_name,
                        password=temp_password,#user_form.cleaned_data['password1']
                    )
    login(request,user)

    #print(f"Username: {temp_name}")
    #return render(request,'calculaber_app/new_account_info.html')

    return HttpResponseRedirect(reverse('calculaber_app:account_info'))



def register(request):
    registered=False#flag to know if registration happened
    if request.method=="POST": #take the information from forms
        user_form=UserForm(data=request.POST)
        print(request.POST)
        if user_form.is_valid(): #check if info from forms is valid
            user=user_form.save()#save dirrectly to database
            temp_password='0000'
            user.set_password(temp_password)
            user.save()#save changes

            registered=True
        else:
            print(user_form.errors)
    else:
        user_form=UserForm()
    return render(request,'calculaber_app/registration.html',{'user_form':user_form,
                                                        'registered':registered})#it's common to have context dictionary keys match with values, so we don't mess it up

def user_login(request):
    if request.method=='POST':#if someone click submit button
        #username=request.POST.get('username')#we use get because in login.html we use simple HTML and we called is 'username' and that's what we are getting
        username=request.POST.get('username')
        temp_password='0000'
        #password=request.POST.get('password')

        user=authenticate(username=username,password=temp_password)  #search for this user

        if user:#if the user is in database
            if user.is_active:#if user is active
                login(request,user)
                return HttpResponseRedirect(reverse('calculaber_app:index'))#return to index.html
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print(f"Username {username}")
            return render(request,'calculaber_app/login.html',{'failed_msg':"Incorrect password"})
            #return HttpResponse("Invalid login details!")
    else:
        return render(request,'calculaber_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('calculaber_app:index'))

@login_required
def special(request):
    return HttpResponse("You are logged in , Nice!")
