from django.shortcuts import render
from UploadData import helper_methods as h
from collections import Counter
import networkx as nx
# Create your views here.

def charts_view(request):
    context = dict()
    if "GET" == request.method:
        return render(request,'charts.html',context)


def display_relation_view(request):
    context = dict()
    
    G = h.create_graph()
    counter = Counter(sorted(nx.get_edge_attributes(G,'relation').values()))
    context['data']=dict(counter)

    if "GET" == request.method:
        return render(request,'relation_chart.html',context)


def display_degree_view(request):

    context = dict()
    G = h.create_graph()
    data = G.degree
    context['data'] = dict(sorted(data))

    if "GET" == request.method:
        return render(request,'display_charts.html',context)

    else:
        return render(request,'display_charts.html',context)

