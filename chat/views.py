from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Chat,  Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core import serializers
import json



@login_required(login_url='/login/')
def index(request):
    username = request.user.first_name if request.user.is_authenticated else "DefaultUsername" 
    if request.method == 'POST':    
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        newMessage = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serializedMessage = json.dumps([{
            "model": "chat.message",
            "pk": newMessage.pk,
            "fields": {
                "text": newMessage.text,
                "created_at": str(newMessage.created_at),
                "author": request.user.first_name,
                "receiver": newMessage.receiver_id,
                "chat": newMessage.chat_id,
            }
        }])
        return JsonResponse(serializedMessage[1:-1], safe=False, content_type='application/json')
    chatMessages = Message.objects.filter(chat__id=1) 
    return render(request, 'chat/index.html', {'messages': chatMessages,'username': username }) 


def loginView(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            if redirect:
                return HttpResponseRedirect(request.POST.get('redirect'))
            else:
                return HttpResponseRedirect('/chat/')
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})


def registerView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('repeatPassword')
        try:
#            validate_password(password)
            if password == repeatPassword:
#                hashed_password = make_password(password)
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
#                user.set_password(hashed_password)
#                user.save()
                return render(request, 'auth/login.html')
            else:
                return render(request, 'auth/register.html', {'passwordNoMatch': True})  
        except Exception as e:
                return render(request, 'auth/register.html', {'passwordNoValidate': True})  
    return render(request, 'auth/register.html')


def logoutView(request):
    print('link works')
    logout(request)
    return HttpResponseRedirect('/login/')