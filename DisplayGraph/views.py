from django.shortcuts import render
from UploadData.views import context 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import io

# Create your views here.
def display_graph_view(request):
    if "GET" == request.method:

        buf = io.BytesIO()

        nx.draw(context['G'])

        plt.savefig(buf,format='svg', bbox_inches='tight') 

        image_bytes = buf.getvalue().decode('utf-8')

        buf.close()

        plt.close()

        context['graph'] = image_bytes

        return render(request, 'display_graph.html',context)

