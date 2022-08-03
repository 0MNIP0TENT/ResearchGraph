from django.shortcuts import render
import networkx as nx
import openpyxl
from users.models import Entity, SemanticType, Relation, Triple 

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

        semantic_types = list()
        entities = list()
        relations = list()
        triples = list()

        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data) 

        G = nx.MultiDiGraph() 

        # create and save semantic type objects first, because they must be added to entities
        typesA = list()
        typesB = list()
        typesAll = list()

        entity_type_mapA = {}
        entity_type_mapB = {}


        for triple in excel_data:
            type_list = triple[0].split("|")[1:]
            for t in type_list: 
                typesA.append(t)

            entity_type_mapA[triple[0].split("|")[0]] = type_list

        for triple in excel_data:
            type_list = triple[2].split("|")[1:]
            for t in type_list: 
                typesB.append(t)

            entity_type_mapB[triple[2].split("|")[0]] = type_list

        # might need to be list form beginning
        akeys = list(entity_type_mapA.keys())
        bkeys = list(entity_type_mapB.keys())
        allkeys = [val for pair in zip(akeys,bkeys) for val in pair]

        avals = list(entity_type_mapA.values())
        bvals = list(entity_type_mapB.values())
        allvals = [val for pair in zip(avals,bvals) for val in pair]

        alldatadict = {k:v for k,v in zip(allkeys,allvals)}


        print('zipped', list(zip(akeys,bkeys)))
        print(alldatadict)

        typesAll = [val for pair in zip(typesA,typesB) for val in pair]

        # remove duplicates if they exist
        no_dupe_types = list()
        [no_dupe_types.append(t) for t in typesAll if t not in no_dupe_types]

        # create semantic types in database
        for t in no_dupe_types:
            semantic_types.append(SemanticType(user=request.user,name=t))

        
        SemanticType.objects.bulk_create(semantic_types)
        semantic_type_objects = SemanticType.objects.all()
       
        for triple in excel_data:
            entities.append(Entity(user=request.user,name=triple[0].split("|")[0]))
            relations.append(Relation(user=request.user,name=triple[1]))
            entities.append(Entity(user=request.user,name=triple[2].split("|")[0]))

        # save entitys before adding semantic types 
        Entity.objects.bulk_create(entities)

        # adding semantic_types to entities in database
        entity_objects = Entity.objects.all()

        for n in range(len(entity_objects)):
            entity_objects[n].semantic_type.set = semantic_type_objects

       # adding the specific types to the entities
        for ent in entity_objects:
            for t in alldatadict[ent.name]:
                objs = SemanticType.objects.filter(name=str(t))
                for obj in objs:
                    ent.semantic_type.add(obj)


        Relation.objects.bulk_create(relations)

        # create the triples
        for n in range(len(Relation.objects.all())):
            triples.append(Triple(user=request.user,entityA=Entity.objects.all()[n],entityB=Entity.objects.all()[n+1], relation=Relation.objects.all()[n]))

        Triple.objects.bulk_create(triples)
        #[triples.append(Triple(user=request.user,entityA=trip[0],relation=trip[1],entityB=trip[2]) for trip in zip())]


        al = list()
      #  for data in range(len(entA)):
      #      al.append((entA[data],entB[data],relations[data]))

        G.add_edges_from(al)

        entitys = list(G.nodes())
        
        context["excel_data"] = excel_data 
        context["entitys"] = entitys 
        context["G"] = G 
        
        return render(request, 'upload_data.html', context)
