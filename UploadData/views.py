from django.shortcuts import render
import openpyxl
from UploadData import helper_methods as h
from Audit.models import AuditTriple, Type, Dataset
from users.models import CustomUser

# Create your views here.

context = {}

def upload_data_view(request):
    if "GET" == request.method:
       return render(request,'upload_data.html',context)
    
    else:
        #user_list = [usr for usr in CustomUser.objects.all() if  not usr.is_staff]
        user_list = CustomUser.objects.all()

        excel_file = request.FILES["excel_file"]

        name = request.POST.get("datasetname")

        name = Dataset.objects.create(name=name) 

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

      #  # Worry about implementing types later 
      #  # create and save semantic type objects first, because they must be added to triples
      #  types = list()

      #  # going through excel triples adding semantic types to list
      #  for triple in excel_data:
      #      type_list = triple[0].split("|")[1:] + triple[2].split("|")[1:]
      #      for t in type_list: 
      #          types.append(t)

      #  # removing duplicates if they exist in semantic_types
      #  types_no_dupes = list()
      #  [types_no_dupes.append(t) for t in types if t not in types_no_dupes]

        # create list of semantic_type_objects 
      #  type_objects = list()

      #  for t in types_no_dupes:
      #      # add for every user
      #      for usr in user_list: 
      #         type_objects.append(Type(dataset=name,user=usr,name=t))

      #  # create semantic type object 
      #  Type.objects.bulk_create(type_objects)
      #  types = list()

        triple_data = list()

        for data in excel_data:
            entA = data[0].split('|')[0] 
        #    entA_types = data[0].split('|')[1:] 

            rel = data[1]

            entB = data[2].split('|')[0] 
        #    entB_types = data[2].split('|')[1:] 

            for usr in user_list:
                 triple_data.append([usr,entA,rel,entB])
                 #triple_data.append([usr,entA,entA_types,rel,entB,entB_types])

        triple_object_list = list()
        for data in triple_data:
            triple_object_list.append(AuditTriple(
                dataset=name,
                user = data[0],
                entityA = data[1],
              #  entityA_types = data[2],
                relation = data[2],
                entityB = data[3],
              #  entityB_types = data[5],

            ))

        AuditTriple.objects.bulk_create(triple_object_list)
        
     #   audit_tiple_query = AuditTriple.objects.all().prefetch_related('entityA_types','entityB_types')

     #   for x in range(len(triple_data)):
     #       for t in triple_data[x][2]: 
     #           usr = triple_data[x][0]
     #           audit_tiple_query[x].entityA_types.add(Type.objects.get(dataset=name,user=usr))
     #           #audit_tiple_query[x].entityA_types.add(Type.objects.get(dataset=name,user=usr,name=t))

     #   for x in range(len(triple_data)):
     #       for t in triple_data[x][5]: 
     #           usr = triple_data[x][0]
     #           audit_tiple_query[x].entityB_types.add(Type.objects.get(dataset=name,user=usr))
                #audit_tiple_query[x].entityB_types.add(Type.objects.get(dataset=name,user=usr,name=t))
      
        return render(request, 'upload_data.html', context)
