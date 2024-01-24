from django.shortcuts import render
from .models import Chat, Message

def index(request):
    username = request.user.first_name if request.user.is_authenticated else "DefaultUsername"
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages,'username': username })
