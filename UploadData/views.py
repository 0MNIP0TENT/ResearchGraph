from django.shortcuts import render
import openpyxl
from UploadData import helper_methods as h
from users.models import Entity, SemanticType, Relation, Triple 
from Audit.models import AuditTriple, Type
from users.models import CustomUser

# Create your views here.

context = {}

def upload_data_view(request):
    if "GET" == request.method:
       return render(request,'upload_data.html',context)
    
    else:
        user = request.user
        user_list = [usr for usr in CustomUser.objects.all() if  not usr.is_staff]

        print(user_list)

        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]

        excel_data = list()

        # iterating over the rows and
        # getting value from each cell in row
        # excel_data is list of lists containing the triples
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data) 

        # create and save semantic type objects first, because they must be added to triples
        types = list()

        # going through excel triples adding semantic types to list
        for triple in excel_data:
            type_list = triple[0].split("|")[1:] + triple[2].split("|")[1:]
            for t in type_list: 
                types.append(t)

        # removing duplicates if they exist in semantic_types
        types_no_dupes = list()
        [types_no_dupes.append(t) for t in types if t not in types_no_dupes]

        # create list of semantic_type_objects 
        type_objects = list()

        for t in types_no_dupes:
            # add for every user
            for usr in user_list: 
               type_objects.append(SemanticType(user=usr,name=t))

        # create semantic type object 
        Type.objects.bulk_create(type_objects)
        types = list()

        triple_data = list()

        for data in excel_data:
            entA = data[0].split('|')[0] 
            entA_types = data[0].split('|')[1:] 

            rel = data[1]

            entB = data[2].split('|')[0] 
            entB_types = data[2].split('|')[1:] 

            for usr in user_list:
                 triple_data.append([usr,entA,entA_types,rel,entB,entB_types])

        triple_object_list = list()
        for data in triple_data:
            triple_object_list.append(AuditTriple(

                user = data[0],
                entityA = data[1],
              #  entityA_types = data[2],
                relation = data[3],
                entityB = data[4],
              #  entityB_types = data[5],

            ))

        AuditTriple.objects.bulk_create(triple_object_list)
        
        audit_tiple_query = AuditTriple.objects.all().prefetch_related('entityA_types','entityB_types')

        for x in range(len(triple_data)):
            for t in triple_data[x][2]: 
                usr = triple_data[x][0]
                audit_tiple_query[x].entityA_types.add(Type.objects.get(user=usr,name=t))

        for x in range(len(triple_data)):
            for t in triple_data[x][5]: 
                usr = triple_data[x][0]
                audit_tiple_query[x].entityB_types.add(Type.objects.get(user=usr,name=t))
      
#
#        # iterating over the rows and
#        # getting value from each cell in row
#        # excel_data is list of lists containing the triples
#        for row in worksheet.iter_rows():
#            row_data = list()
#            for cell in row:
#                row_data.append(str(cell.value))
#            excel_data.append(row_data) 
#
#
#        # create and save semantic type objects first, because they must be added to entities
#        semantic_types = list()
#
#        # going through excel triples adding semantic types to list
#        for triple in excel_data:
#            type_list = triple[0].split("|")[1:] + triple[2].split("|")[1:]
#            for t in type_list: 
#                semantic_types.append(t)
#
#
#        # removing duplicates if they exist in semantic_types
#        types_no_dupes = list()
#        [types_no_dupes.append(t) for t in semantic_types if t not in types_no_dupes]
#
#        # create list of semantic_type_objects 
#        semantic_type_objects = list()
#        for t in types_no_dupes:
#            semantic_type_objects.append(SemanticType(user=request.user,name=t))
#
#        # create semantic type object 
#        SemanticType.objects.bulk_create(semantic_type_objects)
#
#        # getting the objects directly from database
#        semantic_type_objects = SemanticType.objects.all()
#
#        # repeating for entities
#
#        entities = list()
#        entities_no_dupes = list()
#        entity_objects = list()
#
#        # adding all entities from excel triples
#        for triple in excel_data:
#            entities.append(triple[0].split("|")[0])
#            entities.append(triple[2].split("|")[0])
#
#        
#        # removing duplicates if they exist
#        [entities_no_dupes.append(ent) for ent in entities if ent not in entities_no_dupes]
#
#        # cleaning entity names so that they may be passed in the url
#        entities_no_dupes = h.fix_names(entities_no_dupes)
#
#        # creating a list of entity objects 
#        for ent in entities_no_dupes:
#            entity_objects.append(Entity(user=request.user,name=ent))
#
#        # save entitys before adding semantic types 
#        just_saved = Entity.objects.bulk_create(entity_objects)
#
#        # repeat with relations
#
#        relations = list()
#        relations_no_dupes = list()
#        relation_objects = list()
#        for triple in excel_data:
#            relations.append(triple[1])
#
#        [relations_no_dupes.append(rel) for rel in relations if rel not in relations_no_dupes]
#
#        # cleaning relation names so that they may be passed in the url
#        relations_no_dupes = h.fix_relations(relations_no_dupes)
#
#        # creating a list of relation objects
#        for rel in relations_no_dupes:
#            relation_objects.append(Relation(user=request.user,name=rel))
#
#        # save relations in database 
#        Relation.objects.bulk_create(relation_objects)
#
#        # initializing dict with entities as keys and a empty list as a the value
#        entity_type_dict = { ent:list() for ent in entities_no_dupes }
#
#        # map the entities to its types 
#        for ent in entity_type_dict:
#            for triple in excel_data:
#                if ent == triple[0].split("|")[0]:
#                    for t in triple[0].split("|")[1:]:
#                        if t not in entity_type_dict[ent]:
#                            entity_type_dict[ent].append(t)
#
#                
#                if ent == triple[2].split("|")[0]:
#                    for t in triple[2].split("|")[1:]:
#                        if t not in entity_type_dict[ent]:
#                            entity_type_dict[ent].append(t)
#       
#
#        # getting the filtered database objects 
#        entity_objects = Entity.objects.filter(user=request.user)
#        semantic_type_objects = SemanticType.objects.filter(user=request.user)
#
#        for n in range(len(just_saved)):
#            entity_objects[n].semantic_type.set = semantic_type_objects
#
#       # adding the specific types to the entities
#        for ent in entity_objects:
#            if ent.name not in entity_type_dict:
#                continue
#            for t in entity_type_dict[ent.name]:
#                objs = SemanticType.objects.filter(user=request.user,name=str(t))
#                for obj in objs:
#                    ent.semantic_type.add(obj)
#
#
#        # create the triples
#        triples = list()
#        triples_no_dupes = list()
#        triple_objects = list()
#
#        for triple in excel_data:
#            triples.append((h.fix_name(triple[0].split("|")[0]), h.fix_name(triple[1]), h.fix_name(triple[2].split("|")[0])))
#        [triples_no_dupes.append(trip) for trip in triples if trip not in triples_no_dupes]
#
#        # create a list of triple objects
#        relation_objects = Relation.objects.filter(user=request.user)
#        for trip in triples_no_dupes: 
#            triple_objects.append(Triple(user=request.user,entityA=entity_objects.get(name=trip[0]),relation=relation_objects.get(name=trip[1]),entityB=entity_objects.get(name=trip[2])))
#
#        Triple.objects.bulk_create(triple_objects)
#
#
#        context["excel_data"] = excel_data 
#
#        
        return render(request, 'upload_data.html', context)
#
## make new Audit triples
#
