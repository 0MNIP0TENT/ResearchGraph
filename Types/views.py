from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx

# Create your views here.

def display_types_view(request,s_type=None):

    context = dict()

    G = h.create_graph()

    node_attribs = nx.get_node_attributes(G,'types') 
    s_types = list()
    [s_types.extend(t) for t in node_attribs.values()]
    entitys_with_type = [k for k,v in node_attribs.items() if s_type in v]

    if "GET" == request.method:
        context['s_types'] = sorted(set(s_types))
        context['s_type'] = s_type
        if s_type != None:
            context['entitys_with_type'] = entitys_with_type 

            return render(request,'display_types.html',context)

        else:
            return render(request,'display_types.html',context)
