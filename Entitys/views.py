from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx

# Create your views here.

def display_entitys_view(request,entity=None):

    context = dict()

    G = h.create_graph()

    context['entitys'] = sorted(list(G.nodes()))

    in_edges = G.in_edges(entity,data=True)
    out_edges = G.out_edges(entity,data=True)

    if "GET" == request.method:
        if entity != None:
            context['entity'] = entity
            context['types'] = h.get_entity_data(G,entity) 
            context['relation_set'] = set([v for k,v in nx.get_edge_attributes(G,'relation').items() if entity in k])

            context['draw_in_edges'] = h.get_image_planar(in_edges) 
            context['draw_out_edges'] = h.get_image_planar(out_edges) 

            context['out_edges_data'] = sorted([(trip[0],trip[2]['relation'],trip[1]) for trip in out_edges])
            context['in_edges_data'] =  sorted([(trip[0],trip[2]['relation'],trip[1]) for trip in in_edges])
            context['unique_degree'] = len(context['in_edges_data']) + len(context['out_edges_data'])

            return render(request,'display_entitys.html',context)

        else:
            return render(request,'display_entitys.html',context)

