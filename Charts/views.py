from django.shortcuts import render
from UploadData import helper_methods as h
from collections import Counter
import networkx as nx
# Create your views here.

def charts_verified_view(request):
    context = dict()
    if "GET" == request.method:
        return render(request,'verified_charts.html',context)


def display_verified_relation_view(request):
    context = dict()
    G = h.create_graph('Verified')
    counter = Counter(sorted(nx.get_edge_attributes(G,'relation').values()))
    context['data']=dict(counter)

    if "GET" == request.method:
        return render(request,'verified_relation_chart.html',context)


def display_verified_degree_view(request):

    context = dict()
    G = h.create_graph('Verified')
    data = G.degree
    context['data'] = dict(sorted(data))

    if "GET" == request.method:
        return render(request,'display_verified_charts.html',context)

    else:
        return render(request,'display_verified_charts.html',context)

def display_verified_out_relations_view(request):
    context = dict()
    G = h.create_graph('Verified') 
    node_relations = dict()
    relations = list()
    for node in G.nodes():
        out_edges = G.out_edges(node,data='relation')
        relations = [rel[2] for rel in out_edges]
        node_relations[node] = dict(Counter(relations))

    counter = Counter(node_relations)

    context['nodes'] = sorted({k:counter[k] for k in counter})
    context['data'] = {k:counter[k] for k in counter}

    if "GET" == request.method:
        return render(request,'display_verified_out_relations.html',context)

def charts_unverified_view(request):
    context = dict()
    if "GET" == request.method:
        return render(request,'display_unverifid_charts.html',context)


def display_unverified_relation_view(request):
    context = dict()
    G = h.create_graph('UnVerified')
    counter = Counter(sorted(nx.get_edge_attributes(G,'relation').values()))
    context['data']=dict(counter)

    if "GET" == request.method:
        return render(request,'unverified_relation_chart.html',context)


def display_unverified_degree_view(request):

    context = dict()
    G = h.create_graph('UnVerified')
    data = G.degree
    context['data'] = dict(sorted(data))

    if "GET" == request.method:
        return render(request,'display_unverified_charts.html',context)

    else:
        return render(request,'display_unverified_charts.html',context)

def display_unverified_out_relations_view(request):
    context = dict()
    G = h.create_graph('UnVerified') 
    node_relations = dict()
    relations = list()
    for node in G.nodes():
        out_edges = G.out_edges(node,data='relation')
        relations = [rel[2] for rel in out_edges]
        node_relations[node] = dict(Counter(relations))

    counter = Counter(node_relations)

    context['nodes'] = sorted({k:counter[k] for k in counter})
    context['data'] = {k:counter[k] for k in counter}

    if "GET" == request.method:
        return render(request,'display_unverified_out_relations.html',context)


