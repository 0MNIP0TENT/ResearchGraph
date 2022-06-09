from .models import Triple
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
   'atopic':'ATOPIC',
   'carb':'CARB',
   'opco':'OPCO',
   'strd':'STRD', #STEROIDS
   'adjuvant':'ADJUVANT',
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



def fix_names(col):
    # the slashes in the names are converted to hyphens be changed in order
    # to be passed through the url.
    names = list()
    for row in col:
        name = row.split("|")[1]
        if '/' in name:
            a = name.replace('/','-')
            names.append(a)

        elif name == '':
            name = 'NO NAME'
            names.append(name)

        else:
            names.append(name)

    return names

def get_semantic_types(entity):
    """
        If we know the the full name from the dictionary, we use that.
    """
    temp = entity.replace(",","|")
    translated = [semantic_types[t.lstrip().lower()].upper() if t.lstrip().lower() in semantic_types else t.lstrip() for t in set(temp.split('|')[2:])]
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

def get_hist_image(G):
    return nx.degree_histogram(G)



def get_entity_data(G, entity):
    return G.nodes[entity]['types']


def create_graph():
    G = nx.MultiDiGraph()

    colA = [d['entityA'].upper() for d in Triple.objects.values('entityA')] 
    colB = [d['relation'] for d in Triple.objects.values('relation')] 
    colC = [d['entityB'].upper() for d in Triple.objects.values('entityB')] 
          
    entA = fix_names(colA)
    rel = fix_relations(colB) 
    entB = fix_names(colC)

    # add nodes first to add node attribs
    for data in range(len(entA)):
        G.add_node(entA[data],types=get_semantic_types(colA[data])) 
        G.add_node(entB[data],types=get_semantic_types(colC[data])) 

    for data in range(len(entA)):
        G.add_edge(entA[data],entB[data],relation=rel[data])

    return G

