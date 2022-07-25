from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx

# Create your views here.

def display_verified_relations_view(request,relation=None):

    context = dict()

    G = h.create_graph(request,'Verified')
    edge_attribs = nx.get_edge_attributes(G,'relation')
    relation_data = list()
    [relation_data.append([tup[0][0],tup[0][1],tup[1]]) for tup  in set(edge_attribs.items()) if tup[1] == relation]
    context['relations'] = sorted(set(edge_attribs.values()))

    if "GET" == request.method:
        if relation != None:

            context['relation'] = relation
            context['relation_data'] = sorted(relation_data)
            context['count'] = len(relation_data)
            context['relation_edges'] = h.get_image(relation_data)

            return render(request,'display_verified_relations.html',context)

        else:
            return render(request,'display_verified_relations.html',context)

def display_unverified_relations_view(request,relation=None):

    context = dict()

    G = h.create_graph(request,'UnVerified')
    edge_attribs = nx.get_edge_attributes(G,'relation')
    relation_data = list()
    [relation_data.append([tup[0][0],tup[0][1],tup[1]]) for tup  in set(edge_attribs.items()) if tup[1] == relation]
    context['relations'] = sorted(set(edge_attribs.values()))

    if "GET" == request.method:
        if relation != None:

            context['relation'] = relation
            context['relation_data'] = sorted(relation_data)
            context['count'] = len(relation_data)
            context['relation_edges'] = h.get_image(relation_data)

            return render(request,'display_unverified_relations.html',context)

        else:
            return render(request,'display_unverified_relations.html',context)

