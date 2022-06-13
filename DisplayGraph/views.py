from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx

# Create your views here.
def display_graph_view(request):
    if "GET" == request.method:
        context = dict()
        G = h.create_graph()
        context['info'] = nx.info(G)
        context['bar'] = h.get_bar_image(G)

        return render(request, 'display_graph.html',context)

