from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        print("Reiceived data " + request.POST['textmessage'])
    return render(request, 'chat/index.html', {'username': 'Anne'})
