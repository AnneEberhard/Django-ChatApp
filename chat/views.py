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
    """
    This functions renders the chat.html.
    """
    username = request.user.first_name if request.user.is_authenticated else "DefaultUsername" 
    if request.method == 'POST':    
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


#def loginView(request):
#    """
#    This functions renders the login.html.
#    """
#    redirect = request.GET.get('next')
#    if request.method == 'POST':
#        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
#        if user:
#            login(request, user)
#            if redirect:
#                return HttpResponseRedirect(request.POST.get('redirect'))
#            else:
#                return HttpResponseRedirect('/chat/')
#        else:
#            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
#    return render(request, 'auth/login.html', {'redirect': redirect})


def login_view(request):
    """
    This function processes the login request and returns a JSON response for POST and a HTTP for other requests.
    """
    redirect = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': redirect or '/chat/'}, safe=False, content_type='application/json')
        else:
            return JsonResponse({'success': False, 'message': 'Wrong username or password'}, safe=False, content_type='application/json')
    else:
        return render(request, 'auth/login.html', {'redirect': redirect})


#def registerView(request):
#    """
#    This functions renders the register.html.
#    """
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        first_name = request.POST.get('first_name')
#        last_name = request.POST.get('last_name')
#        email = request.POST.get('email')
#        password = request.POST.get('password')
#        repeatPassword = request.POST.get('repeatPassword')
#        try:
#            if password == repeatPassword:
#                User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
#                return render(request, 'auth/login.html')
#            else:
#                return render(request, 'auth/register.html', {'passwordNoMatch': True})  
#        except Exception as e:
#                return render(request, 'auth/register.html', {'passwordNoValidate': True})  
#    return render(request, 'auth/register.html')

def register_view(request):
    """
    This functions processes the register request and returns a JSON response for POST and a HTTP for other requests.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('repeat_password')
        try:
            if password == repeatPassword:
                User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                return JsonResponse({'success': True, 'redirect': '/login/'}, safe=False, content_type='application/json')
            else:
                return JsonResponse({'success': False, 'passwordNoMatch': True}, safe=False, content_type='application/json')
        except Exception as e:
                return JsonResponse({'success': False, 'error': True}, safe=False, content_type='application/json')
    else:
        return render(request, 'auth/register.html')


def logout_view(request):
    """
    This functions initates logout and returns to login.html.
    """
    logout(request)
    return HttpResponseRedirect('/login/')