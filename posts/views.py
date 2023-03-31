from django.http import HttpResponse


def index(request):
    return HttpResponse("Yoh!! Así se ve una vista cruda y desnuda en Django.")
