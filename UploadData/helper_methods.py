from .models import Triple
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

semantic_types = {
   'aapp':'aapp:Amino Acid, Peptide, or Protein',
   'acab':'acab:Acquired Abnormality',
   'acty':'acty:Activity',
   'aggp':'aggp:Age Group',
   'amas':'amas:Amino Acid Sequence',
   'amph':'amph:Amphibian',
   'anab':'anab:Anatomical Abnormality',
   'anim':'anim:Animal',
   'anst':'anst:Anatomical Structure',
   'antb':'antb:Antibiotic',
   'arch':'arch:Archaeon',
   'bacs':'bacs:Biologically Active Substance',
   'bact':'bact:Bacterium',
   'bdsu':'bdsu:Body Substance',
   'bdsy':'bdsy:Body System',
   'bhvr':'bhvr:Behavior',
   'biof':'biof:Biologic Function',
   'bird':'bird:Bird',
   'blor':'blor:Body Location or Region',
   'bmod':'bmod:Biomedical Occupation or Discipline',
   'bodm':'bodm:Biomedical or Dental Material',
   'bpoc':'bpoc:Body Part, Organ, or Organ Component',
   'bsoj':'bsoj:Body Space or Junction',
   'celc':'celc:Cell Component',
   'celf':'celf:Cell Function',
   'cell':'cell:Cell',
   'cgab':'cgab:Congenital Abnormality',
   'chem':'chem:Chemical',
   'chvf':'chvf:Chemical Viewed Functionally',
   'chvs':'chvs:Chemical Viewed Structurally',
   'clas':'clas:Classification',
   'clna':'clna:Clinical Attribute',
   'clnd':'clnd:Clinical Drug',
   'cnce':'cnce:Conceptual Entity',
   'comd':'comd:Cell or Molecular Dysfunction',
   'crbs':'crbs:Carbohydrate Sequence',
   'diap':'diap:Diagnostic Procedure',
   'dora':'dora:Daily or Recreational Activity',
   'drdd':'drdd:Drug Delivery Device',
   'dsyn':'dsyn:Disease or Syndrome',
   'edac':'edac:Educational Activity',
   'eehu':'eehu:Environmental Effect of Humans',
   'elii':'elii:Element, Ion, or Isotope',
   'emod':'emod:Experimental Model of Disease',
   'emst':'emst:Embryonic Structure',
   'enty':'enty:Entity',
   'enzy':'enzy:Enzyme',
   'euka':'euka:Eukaryote',
   'evnt':'evnt:Event',
   'famg':'famg:Family Group',
   'ffas':'ffas:Fully Formed Anatomical Structure',
   'fish':'fish:Fish',
   'fndg':'fndg:Finding',
   'fngs':'fngs:Fungus',
   'food':'food:Food',
   'ftcn':'ftcn:Functional Concept',
   'genf':'genf:Genetic Function',
   'geoa':'geoa:Geographic Area',
   'gngm':'gngm:Gene or Genome',
   'gora':'gora:Governmental or Regulatory Activity',
   'grpa':'grpa:Group Attribute',
   'grup':'grup:Group',
   'hcpp':'hcpp:Human-caused Phenomenon or Process',
   'hcro':'hcro:Health Care Related Organization',
   'hlca':'hlca:Health Care Activity',
   'hops':'hops:Hazardous or Poisonous Substance',
   'horm':'horm:Hormone',
   'humn':'humn:Human',
   'idcn':'idcn:Idea or Concept',
   'imft':'imft:Immunologic Factor',
   'inbe':'inbe:Individual Behavior',
   'inch':'inch:Inorganic Chemical',
   'inpo':'inpo:Injury or Poisoning',
   'inpr':'inpr:Intellectual Product',
   'irda':'irda:Indicator, Reagent, or Diagnostic Aid',
   'lang':'lang:Language',
   'lbpr':'lbpr:Laboratory Procedure',
   'lbtr':'lbtr:Laboratory or Test Result',
   'mamm':'mamm:Mammal',
   'mbrt':'mbrt:Molecular Biology Research Technique',
   'mcha':'mcha:Machine Activity',
   'medd':'medd:Medical Device',
   'menp':'menp:Mental Process',
   'mnob':'mnob:Manufactured Object',
   'mobd':'mobd:Mental or Behavioral Dysfunction',
   'moft':'moft:Molecular Function',
   'mosq':'mosq:Molecular Sequence',
   'neop':'neop:Neoplastic Process',
   'nnon':'nnon:Nucleic Acid, Nucleoside, or Nucleotide',
   'npop':'npop:Natural Phenomenon or Process',
   'nusq':'nusq:Nucleotide Sequence',
   'ocac':'ocac:Occupational Activity',
   'ocdi':'ocdi:Occupation or Discipline',
   'orch':'orch:Organic Chemical',
   'orga':'orga:Organism Attribute',
   'orgf':'orgf:Organism Function',
   'orgm':'orgm:Organism',
   'orgt':'orgt:Organization',
   'ortf':'ortf:Organ or Tissue Function',
   'patf':'patf:Pathologic Function',
   'phob':'phob:Physical Object',
   'phpr':'phpr:Phenomenon or Process',
   'phsf':'phsf:Physiologic Function',
   'phsu':'phsu:Pharmacologic Substance',
   'plnt':'plnt:Plant',
   'podg':'podg:Patient or Disabled Group',
   'popg':'popg:Population Group',
   'prog':'prog:Professional or Occupational Group',
   'pros':'pros:Professional Society',
   'qlco':'qlco:Qualitative Concept',
   'qnco':'qnco:Quantitative Concept',
   'rcpt':'rcpt:Receptor',
   'rept':'rept:Reptile',
   'resa':'resa:Research Activity',
   'resd':'resd:Research Device',
   'rnlw':'rnlw:Regulation or Law',
   'sbst':'sbst:Substance',
   #  
  # 'carb':'carb',
  # 'opco':'opco',
  # 'strd':'strd', steroids
  # 'adjuvant':'adjuvant',
   #
   'shro':'shro:Self-help or Relief Organization',
   'socb':'socb:Social Behavior',
   'sosy':'sosy:Sign or Symptom',
   'spco':'spco:Spatial Concept',
   'tisu':'tisu:Tissue',
   'tmco':'tmco:Temporal Concept',
   'topp':'topp:Therapeutic or Preventive Procedure',
   'virs':'virs:Virus',
   'vita':'vita:Vitamin',
   'vtbt':'vtbt:Vertebrate',
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
    translated = [semantic_types[t.strip().lower()] if t.strip().lower() in semantic_types else t for t in set(temp.split('|')[2:])]
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

