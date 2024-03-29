from .models import Verified
from Audit.models import AuditTriple
from collections import Counter
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

semantic_types = {
   'aapp':'AAPP:AMINO ACID, PEPTIDE, OR PROTEIN',
   'acab':'ACAB:ACQUIRED ABNORMALITY',
   'acty':'ACTY:ACTIVITY',
   'aggp':'AGGP:AGE GROUP',
   'amas':'AMAS:AMINO ACID SEQUENCE',
   'amph':'AMPH:AMPHIBIAN',
   'anab':'ANAB:ANATOMICAL ABNORMALITY',
   'anim':'ANIM:ANIMAL',
   'anst':'ANST:ANATOMICAL STRUCTURE',
   'antb':'ANTB:ANTIBIOTIC',
   'arch':'ARCH:ARCHAEON',
   'bacs':'BACS:BIOLOGICALLY ACTIVE SUBSTANCE',
   'bact':'BACT:BACTERIUM',
   'bdsu':'BDSU:BODY SUBSTANCE',
   'bdsy':'BDSY:BODY SYSTEM',
   'bhvr':'BHVR:BEHAVIOR',
   'biof':'BIOF:BIOLOGIC FUNCTION',
   'bird':'BIRD:BIRD',
   'blor':'BLOR:BODY LOCATION OR REGION',
   'bmod':'BMOD:BIOMEDICAL OCCUPATION OR DISCIPLINE',
   'bodm':'BODM:BIOMEDICAL OR DENTAL MATERIAL',
   'bpoc':'BPOC:BODY PART, ORGAN, OR ORGAN COMPONENT',
   'bsoj':'BSOJ:BODY SPACE OR JUNCTION',
   'celc':'CELC:CELL COMPONENT',
   'celf':'CELF:CELL FUNCTION',
   'cell':'CELL:CELL',
   'cgab':'CGAB:CONGENITAL ABNORMALITY',
   'chem':'CHEM:CHEMICAL',
   'chvf':'CHVF:CHEMICAL VIEWED FUNCTIONALLY',
   'chvs':'CHVS:CHEMICAL VIEWED STRUCTURALLY',
   'clas':'CLAS:CLASSIFICATION',
   'clna':'CLNA:CLINICAL ATTRIBUTE',
   'clnd':'CLND:CLINICAL DRUG',
   'cnce':'CNCE:CONCEPTUAL ENTITY',
   'comd':'COMD:CELL OR MOLECULAR DYSFUNCTION',
   'crbs':'CRBS:CARBOHYDRATE SEQUENCE',
   'diap':'DIAP:DIAGNOSTIC PROCEDURE',
   'dora':'DORA:DAILY OR RECREATIONAL ACTIVITY',
   'drdd':'DRDD:DRUG DELIVERY DEVICE',
   'dsyn':'DSYN:DISEASE OR SYNDROME',
   'edac':'EDAC:EDUCATIONAL ACTIVITY',
   'eehu':'EEHU:ENVIRONMENTAL EFFECT OF HUMANS',
   'elii':'ELII:ELEMENT, ION, OR ISOTOPE',
   'emod':'EMOD:EXPERIMENTAL MODEL OF DISEASE',
   'emst':'EMST:EMBRYONIC STRUCTURE',
   'enty':'ENTY:ENTITY',
   'enzy':'ENZY:ENZYME',
   'euka':'EUKA:EUKARYOTE',
   'evnt':'EVNT:EVENT',
   'famg':'FAMG:FAMILY GROUP',
   'ffas':'FFAS:FULLY FORMED ANATOMICAL STRUCTURE',
   'fish':'FISH:FISH',
   'fndg':'FNDG:FINDING',
   'fngs':'FNGS:FUNGUS',
   'food':'FOOD:FOOD',
   'ftcn':'FTCN:FUNCTIONAL CONCEPT',
   'genf':'GENF:GENETIC FUNCTION',
   'geoa':'GEOA:GEOGRAPHIC AREA',
   'gngm':'GNGM:GENE OR GENOME',
   'gora':'GORA:GOVERNMENTAL OR REGULATORY ACTIVITY',
   'grpa':'GRPA:GROUP ATTRIBUTE',
   'grup':'GRUP:GROUP',
   'hcpp':'HCPP:HUMAN-CAUSED PHENOMENON OR PROCESS',
   'hcro':'HCRO:HEALTH CARE RELATED ORGANIZATION',
   'hlca':'HLCA:HEALTH CARE ACTIVITY',
   'hops':'HOPS:HAZARDOUS OR POISONOUS SUBSTANCE',
   'horm':'HORM:HORMONE',
   'humn':'HUMN:HUMAN',
   'idcn':'IDCN:IDEA OR CONCEPT',
   'imft':'IMFT:IMMUNOLOGIC FACTOR',
   'inbe':'INBE:INDIVIDUAL BEHAVIOR',
   'inch':'INCH:INORGANIC CHEMICAL',
   'inpo':'INPO:INJURY OR POISONING',
   'inpr':'INPR:INTELLECTUAL PRODUCT',
   'irda':'IRDA:INDICATOR, REAGENT, OR DIAGNOSTIC AID',
   'lang':'LANG:LANGUAGE',
   'lbpr':'LBPR:LABORATORY PROCEDURE',
   'lbtr':'LBTR:LABORATORY OR TEST RESULT',
   'mamm':'MAMM:MAMMAL',
   'mbrt':'MBRT:MOLECULAR BIOLOGY RESEARCH TECHNIQUE',
   'mcha':'MCHA:MACHINE ACTIVITY',
   'medd':'MEDD:MEDICAL DEVICE',
   'menp':'MENP:MENTAL PROCESS',
   'mnob':'MNOB:MANUFACTURED OBJECT',
   'mobd':'MOBD:MENTAL OR BEHAVIORAL DYSFUNCTION',
   'moft':'MOFT:MOLECULAR FUNCTION',
   'mosq':'MOSQ:MOLECULAR SEQUENCE',
   'neop':'NEOP:NEOPLASTIC PROCESS',
   'nnon':'NNON:NUCLEIC ACID, NUCLEOSIDE, OR NUCLEOTIde',
   'npop':'NPOP:NATURAL PHENOMENON OR PROCESS',
   'nusq':'NUSQ:NUCLEOTIDE SEQUENCE',
   'ocac':'OCAC:OCCUPATIONAL ACTIVITY',
   'ocdi':'OCDI:OCCUPATION OR DISCIPLINE',
   'orch':'ORCH:ORGANIC CHEMICAL',
   'orga':'ORGA:ORGANISM ATTRIBUTE',
   'orgf':'ORGF:ORGANISM FUNCTION',
   'orgm':'ORGM:ORGANISM',
   'orgt':'ORGT:ORGANIZATION',
   'ortf':'ORTF:ORGAN OR TISSUE FUNCTION',
   'patf':'PATF:PATHOLOGIC FUNCTION',
   'phob':'PHOB:PHYSICAL OBJECT',
   'phpr':'PHPR:PHENOMENON OR PROCESS',
   'phsf':'PHSF:PHYSIOLOGIC FUNCTION',
   'phsu':'PHSU:PHARMACOLOGIC SUBSTANCE',
   'plnt':'PLNT:PLANT',
   'podg':'PODG:PATIENT OR DISABLED GROUP',
   'popg':'POPG:POPULATION GROUP',
   'prog':'PROG:PROFESSIONAL OR OCCUPATIONAL GROUP',
   'pros':'PROS:PROFESSIONAL SOCIETY',
   'qlco':'QLCO:QUALITATIVE CONCEPT',
   'qnco':'QNCO:QUANTITATIVE CONCEPT',
   'rcpt':'RCPT:RECEPTOR',
   'rept':'REPT:REPTILE',
   'resa':'RESA:RESEARCH ACTIVITY',
   'resd':'RESD:RESEARCH DEVICE',
   'rnlw':'RNLW:REGULATION OR LAW',
   'sbst':'SBST:SUBSTANCE',
   # added 
   'adjuvant':'ADJUVANT',
   'atopic':'ATOPIC',
   'biological':'BIOLOGICAL',
   'body':'BODY',
   'breast':'BREAST',
   'ductal':'DUCTAL',
   'carb':'CARB',
   'conformal':'CONFORMAL',
   'cytotoxic':'CYTOTOXIC',
   'emission-computed':'EMISSION-COMPUTED',
   'erbb':'ERBB',
   'general':'GENERAL',
   'human':'HUMAN',
   'internal':'INTERNAL',
   'invt':'INVT',
   'left':'LEFT',
   'lipd':'LIPD',
   'low-level':'LOW-LEVEL',
   'malignant':'MALIGNANT',
   'mass':'MASS',
   'mediterranean':'MEDITERRANEAN',
   'myofascial':'MYOFASCIAL',
   'non-small-cell lung':'NON-SMALL-CELL LUNG',
   'non-steroidal':'NON-STEROIDAL',
   'nos':'NOS',
   'nsba':'NSBA',
   'omega-3':'OMEGA-3',
   'opco':'OPCO', 
   'oral':'ORAL', 
   'phase ii':'PHASE II',
   'phase iii':'PHASE III',
   'pleural':'PLEURAL',
   'postoperative':'POSTOPERATIVE',
   'premature':'PREMATURE',
   'randomized':'RANDOMIZED',
   'single-photon':'SINGLE-PHOTON', 
   'strd':'STRD', #STEROIDS
   'targeted':'TARGETED',
   'tumor-infiltrating':'TUMOR-INFILTRATING',
   'university':'UNIVERSITY',
   # added end
   'shro':'SHRO:SELF-HELP OR RELIEF ORGanization',
   'socb':'SOCB:SOCIAL BEHAVIOR',
   'sosy':'SOSY:SIGN OR SYMPTOM',
   'spco':'SPCO:SPATIAL CONCEPT',
   'tisu':'TISU:TISSUE',
   'tmco':'TMCO:TEMPORAL CONCEPT',
   'topp':'TOPP:THERAPEUTIC OR PREVENTIve Procedure',
   'virs':'VIRS:VIRUS',
   'vita':'VITA:VITAMIN',
   'vtbt':'VTBT:VERTEBRATE',
}

def fix_relations(col):
    # taking out the underscores and replacing with spaces
    relations = list()
    for row in col:
        if '_' in row:
            a = row.replace('_',' ')
            relations.append(a)

        else:
            relations.append(row)

    return relations


def fix_name(name):
    # the slashes in the names are converted to hyphens be changed in order
    # to be passed through the url.

    if '/' in name:
        name = name.replace('/','-')

    if '_' in name:
        name = name.replace('_',' ')

    elif name == '':
        name = 'NO NAME'


    return name

def fix_names(col):
    # the slashes in the names are converted to hyphens be changed in order
    # to be passed through the url.
    names = list()
    for row in col:
        name = row.split("|")[0]

        if '/' in name:
            name = name.replace('/','-')

        if '_' in name:
            name = name.replace('_',' ')

        elif name == '':
            name = 'NO NAME'

        names.append(name)

    return names

def get_semantic_types(entity):
    """
        If we know the the full name from the dictionary, we use that.
    """
    temp = entity.replace(",","|")
    translated = [semantic_types[t.lstrip().lower()].upper() if t.lstrip().lower() in semantic_types else t.lstrip() for t in set(temp.split('|')[1:])]
    return translated 

def get_semantic_types_unverified(types):
    """
        If we know the the full name from the dictionary, we use that.
    """
    temp = types.split('|') 
    translated = list()

    for t in temp:
        if t in semantic_types:
            translated.append(semantic_types[t])
        else:
            translated.append(t)

    return translated


def get_image_planar(edge_list):
    buf = io.BytesIO()
    image  = nx.MultiDiGraph(edge_list)
    nx.draw_planar(image,font_size=8,with_labels=True)
    plt.margins(x=0.3)
    plt.savefig(buf,format='svg',transparent=True) 
    image_bytes = buf.getvalue().decode('utf-8')
    buf.close()
    plt.close()
    return image_bytes

def get_image(edge_list):
    buf = io.BytesIO()
    image  = nx.MultiDiGraph(edge_list,data=True)
    nx.draw(image,font_size=8,with_labels=True)
    plt.margins(x=0.3)
    plt.savefig(buf,format='svg',transparent=True) 
    image_bytes = buf.getvalue().decode('utf-8')
    buf.close()
    plt.close()
    return image_bytes

def get_bar_image(G):

    bars = 5

    buf = io.BytesIO()

    degree_list = list(nx.degree(G))
   
    x = list()
    y = list()

    sorted_list = sort_tuples(degree_list)

    [x.append(a) for a, _ in sorted_list[-bars:]]
    [y.append(b) for _, b in  sorted_list[-bars:]]


    plt.figure(figsize=(10,3))
    colors = dict(zip(x,['cyan','blue','green','orange','red']))
    labels = colors.keys() 
    handles = [plt.Rectangle((0,0),1,1,color=colors[label]) for label in labels]

    plt.barh(x[:5],y[:5], color=list(colors.values()))

    # add value to end of bar
    for index, value in enumerate(y[:5]):
        plt.text(value,index, str(value))

    plt.yticks([])
    plt.ylabel("Entities")
    plt.ylabel("# of times appeared in triple")
    plt.legend(handles, labels)
    plt.title('Entities in the most connections')
    plt.savefig(buf,format='svg',transparent=True) 

    image_bytes = buf.getvalue().decode('utf-8')

    buf.close()
    plt.close()

    return image_bytes

def get_relation_bar(relations):

    bars = 5

    buf = io.BytesIO()

    c = Counter()
    c.update(relations.values())

    relation_counts = [(x,y) for x,y in c.items()]

    sorted_list = sort_tuples(relation_counts)

    x = list()
    y = list()

    [x.append(a) for a, _ in sorted_list[-bars:]]
    [y.append(b) for _, b in  sorted_list[-bars:]]

    plt.figure(figsize=(10,3))
    colors = dict(zip(x,['cyan','blue','green','orange','red']))
    labels = colors.keys() 
    handles = [plt.Rectangle((0,0),1,1,color=colors[label]) for label in labels]

    plt.barh(x[:5],y[:5], color=list(colors.values()))

    plt.yticks([])
    plt.ylabel("Relations")
    plt.ylabel("# of relations found")
    plt.legend(handles, labels)
    plt.title('Relations that appear in the most triples')

    # add value to end of bar
    for index, value in enumerate(y[:5]):
        plt.text(value,index,str(value))

    plt.savefig(buf,format='svg',transparent=True) 

    image_bytes = buf.getvalue().decode('utf-8')

    buf.close()
    plt.close()

    return image_bytes


def sort_tuples(tup):
    """
        function will sort a list of tupels based
        on it's second value.
    """
    return(sorted(tup, key = lambda x: x[1])) 

def get_entity_data(G, entity):
    return G.nodes[entity]['types']


def create_graph(request,dataset):
    G = nx.MultiDiGraph()
    if dataset == "Verified":
        colA = [d['entityA'].upper() for d in Verified.objects.values('entityA')] 
        colB = [d['relation'] for d in Verified.objects.values('relation')] 
        colC = [d['entityB'].upper() for d in Verified.objects.values('entityB')] 

        entA = fix_names(colA)
        entB = fix_names(colC)        

        rel = fix_relations(colB) 

        # add nodes first to add node attribs
        for data in range(len(entA)):
            G.add_node(entA[data],types=get_semantic_types(colA[data])) 
            G.add_node(entB[data],types=get_semantic_types(colC[data])) 

        for data in range(len(entA)):
            G.add_edge(entA[data],entB[data],relation=rel[data])


    else:
     #   triples = Triple.objects.filter(user=request.user).select_related('entityA','relation','entityB') 
     #   # add nodes first to add node attribs
     #   entities = Entity.objects.filter(user=request.user).prefetch_related('semantic_type') 
     #   for ent in entities:

     #       types = [t.name for t in ent.semantic_type.all()]

#            if not types:
#                G.add_node(ent.name,types=['None'])
#            else:
#                types = "|".join(types)
#                G.add_node(ent.name,types=get_semantic_types_unverified(types))

#        for trip in triples:
#            G.add_edge(trip.entityA.name,trip.entityB.name,relation=trip.relation.name)
    
        triples = AuditTriple.objects.filter(user=request.user).prefetch_related('entityA_types','entityB_types') 

        entities = list()

        for trip in triples:
            entities.append(trip.entityA)
            entities.append(trip.entityB)

            typesA = list() 
            typesB = list()

            [typesA.append(t.name) for t in trip.entityA_types.all()]
            [typesB.append(t.name) for t in trip.entityB_types.all()]

            G.add_node(trip.entityA,types=typesA)
            G.add_node(trip.entityB,types=typesB)

        for trip in triples:
            G.add_edge(trip.entityA,trip.entityB,relation=trip.relation)

    return G
