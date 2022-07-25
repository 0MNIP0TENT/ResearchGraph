from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx

# Create your views here.
def display_verified_graph_view(request):
    if "GET" == request.method:
        context = dict()
        G = h.create_graph(request,'Verified')
        context['info'] = nx.info(G)
        context['relation_bar'] = h.get_relation_bar(nx.get_edge_attributes(G,'relation'))
        context['bar'] = h.get_bar_image(G)

        return render(request, 'display_verified_graph.html',context)

def display_unverified_graph_view(request):
    if "GET" == request.method:
        context = dict()
        G = h.create_graph(request,'UnVerified')
        context['info'] = nx.info(G)
        context['relation_bar'] = h.get_relation_bar(nx.get_edge_attributes(G,'relation'))
        context['bar'] = h.get_bar_image(G)

        return render(request, 'display_unverified_graph.html',context)

