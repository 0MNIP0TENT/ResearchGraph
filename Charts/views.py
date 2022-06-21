from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx
# Create your views here.

def display_charts_view(request):

    context = dict()
    
    G = h.create_graph()
    data = G.degree
    context['data'] = dict(sorted(data))

    if "GET" == request.method:
           
        return render(request,'display_charts.html',context)

    else:
        return render(request,'display_charts.html',context)

