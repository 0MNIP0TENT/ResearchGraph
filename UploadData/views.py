from django.shortcuts import render
import networkx as nx
import openpyxl
from users.models import UserDataset as dataset 

# Create your views here.

context = {}

def fix_names(col):
    # some of the entity names must be changed in order
    # to pass them thru the url
    names = list()
    for row in col:
        name = row.split("|")[0]
        if '/' in name:
            a = name.replace('/','-')
            names.append(a)

        elif name == '':
            name = 'NO NAME'
            names.append(name)

        else:
            names.append(name)

    return names

def upload_data_view(request):
    if "GET" == request.method:
       return render(request,'upload_data.html',context)
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]

        excel_data = list()
        colA = list()
        colB = list()
        colC = list()

        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data) 

        G = nx.MultiDiGraph() 

        datasets = list()

        for triple in excel_data:
            colA.append(triple[0])
            colB.append(triple[1])
            colC.append(triple[2])
            datasets.append(dataset(entityA=triple[0],relation=triple[1],entityB=triple[2],dataset=request.user))

        # ds is initialized in loop 
        dataset.objects.bulk_create(datasets)
        entA = fix_names(colA)
        entB = fix_names(colC)
        relations = [triple[1] for triple in excel_data]

        al = list()
        for data in range(len(entA)):
            al.append((entA[data],entB[data],relations[data]))


        G.add_edges_from(al)

        entitys = list(G.nodes())
        
        context["excel_data"] = excel_data 
        context["entitys"] = entitys 
        context["G"] = G 

        return render(request, 'upload_data.html', context)
