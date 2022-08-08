from django.shortcuts import render
from UploadData import helper_methods as h
import networkx as nx

# Create your views here.

def display_verified_entitys_view(request,entity=None):

    context = dict()

    if "GET" == request.method:

        G = h.create_graph(request,'Verified')

        context['entities'] = sorted(list(G.nodes()))

        in_edges = G.in_edges(entity,data=True)
        out_edges = G.out_edges(entity,data=True)

        if entity != None:
            context['entity'] = entity
            context['types'] = h.get_entity_data(G,entity) 
            context['relation_set'] = set([v for k,v in nx.get_edge_attributes(G,'relation').items() if entity in k])

            context['draw_in_edges'] = h.get_image_planar(in_edges) 
            context['draw_out_edges'] = h.get_image_planar(out_edges) 

            out_edges_data = sorted([[trip[0],trip[2]['relation'],trip[1]] for trip in out_edges])
            
            out_edges_nums = [len(G.in_edges(ent[2],default=0)) + len(G.out_edges(ent[2],default=0)) for ent in out_edges_data]
            out_edges_percents = [round(edge/len(G.edges)*100,2) for edge in out_edges_nums]

            for i in range(len(out_edges_data)):
                out_edges_data[i].append(out_edges_nums[i])
                out_edges_data[i].append(out_edges_percents[i])
            

            in_edges_data = sorted([[trip[0],trip[2]['relation'],trip[1]] for trip in in_edges])

            in_edges_nums = [len(G.in_edges(ent[0],default=0)) + len(G.out_edges(ent[0],default=0)) for ent in in_edges_data]
            in_edges_percents = [round(edge/len(G.edges)*100,2) for edge in in_edges_nums]

            for i in range(len(in_edges_data)):
                in_edges_data[i].append(in_edges_nums[i])
                in_edges_data[i].append(in_edges_percents[i])

            context['out_edges_data'] = out_edges_data 
            context['in_edges_data'] = in_edges_data 

            context['unique_degree'] = len(in_edges) + len(out_edges)

            return render(request,'display_verified_entities.html',context)

        else:
            return render(request,'display_verified_entities.html',context)


def display_unverified_entitys_view(request,entity=None):

    context = dict()

    if "GET" == request.method:

        G = h.create_graph(request,'UnVerified')
        # remove None from user choice list
        entities = sorted(list(G.nodes()))
        context['entities'] = [ent for ent in entities if ent != 'None'] 

        in_edges = G.in_edges(entity,data=True)
        out_edges = G.out_edges(entity,data=True)

        if entity != None:
            context['entity'] = entity
            context['types'] = h.get_entity_data(G,entity) 
            context['relation_set'] = set([v for k,v in nx.get_edge_attributes(G,'relation').items() if entity in k])

            context['draw_in_edges'] = h.get_image_planar(in_edges) 
            context['draw_out_edges'] = h.get_image_planar(out_edges) 

            out_edges_data = sorted([[trip[0],trip[2]['relation'],trip[1]] for trip in out_edges])
            
            out_edges_nums = [len(G.in_edges(ent[2],default=0)) + len(G.out_edges(ent[2],default=0)) for ent in out_edges_data]
            out_edges_percents = [round(edge/len(G.edges)*100,2) for edge in out_edges_nums]

            for i in range(len(out_edges_data)):
                out_edges_data[i].append(out_edges_nums[i])
                out_edges_data[i].append(out_edges_percents[i])
            

            in_edges_data = sorted([[trip[0],trip[2]['relation'],trip[1]] for trip in in_edges])

            in_edges_nums = [len(G.in_edges(ent[0],default=0)) + len(G.out_edges(ent[0],default=0)) for ent in in_edges_data]
            in_edges_percents = [round(edge/len(G.edges)*100,2) for edge in in_edges_nums]

            for i in range(len(in_edges_data)):
                in_edges_data[i].append(in_edges_nums[i])
                in_edges_data[i].append(in_edges_percents[i])

            context['out_edges_data'] = out_edges_data 
            context['in_edges_data'] = in_edges_data 

            context['unique_degree'] = len(in_edges) + len(out_edges)

            return render(request,'display_unverified_entities.html',context)

        else:
            return render(request,'display_unverified_entities.html',context)

