from django.shortcuts import render

def index(request):
    return render(request, 'dev/index.html')


def dev(request, dev_name):
    return render(request, 'dev/dev.html', {
        'dev_name': dev_name
    })

