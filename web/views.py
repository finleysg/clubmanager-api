from django.shortcuts import render


def index(request):
    context = {
        # TODO: the user object should go here
    }
    return render(request, "web/index.html", context)
