from django.shortcuts import render

# Create your views here.
def drawings_list(request):
    return render(request, 'base.html')