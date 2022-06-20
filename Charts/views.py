from django.shortcuts import render

# Create your views here.

def display_charts_view(request):

    context = dict()


    if "GET" == request.method:
           
        return render(request,'display_charts.html',context)

    else:
        return render(request,'display_charts.html',context)

