from .models import Triple
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

semantic_types = {
   'aapp':'Amino Acid, Peptide, or Protein',
   'acab':'Acquired Abnormality',
   'acty':'Activity',
   'aggp':'Age Group',
   'amas':'Amino Acid Sequence',
   'amph':'Amphibian',
   'anab':'Anatomical Abnormality',
   'anim':'Animal',
   'anst':'Anatomical Structure',
   'antb':'Antibiotic',
   'arch':'Archaeon',
   'bacs':'Biologically Active Substance',
   'bact':'Bacterium',
   'bdsu':'Body Substance',
   'bdsy':'Body System',
   'bhvr':'Behavior',
   'biof':'Biologic Function',
   'bird':'Bird',
   'blor':'Body Location or Region',
   'bmod':'Biomedical Occupation or Discipline',
   'bodm':'Biomedical or Dental Material',
   'bpoc':'Body Part, Organ, or Organ Component',
   'bsoj':'Body Space or Junction',
   'celc':'Cell Component',
   'celf':'Cell Function',
   'cell':'Cell',
   'cgab':'Congenital Abnormality',
   'chem':'Chemical',
   'chvf':'Chemical Viewed Functionally',
   'chvs':'Chemical Viewed Structurally',
   'clas':'Classification',
   'clna':'Clinical Attribute',
   'clnd':'Clinical Drug',
   'cnce':'Conceptual Entity',
   'comd':'Cell or Molecular Dysfunction',
   'crbs':'Carbohydrate Sequence',
   'diap':'Diagnostic Procedure',
   'dora':'Daily or Recreational Activity',
   'drdd':'Drug Delivery Device',
   'dsyn':'Disease or Syndrome',
   'edac':'Educational Activity',
   'eehu':'Environmental Effect of Humans',
   'elii':'Element, Ion, or Isotope',
   'emod':'Experimental Model of Disease',
   'emst':'Embryonic Structure',
   'enty':'Entity',
   'enzy':'Enzyme',
   'euka':'Eukaryote',
   'evnt':'Event',
   'famg':'Family Group',
   'ffas':'Fully Formed Anatomical Structure',
   'fish':'Fish',
   'fndg':'Finding',
   'fngs':'Fungus',
   'food':'Food',
   'ftcn':'Functional Concept',
   'genf':'Genetic Function',
   'geoa':'Geographic Area',
   'gngm':'Gene or Genome',
   'gora':'Governmental or Regulatory Activity',
   'grpa':'Group Attribute',
   'grup':'Group',
   'hcpp':'Human-caused Phenomenon or Process',
   'hcro':'Health Care Related Organization',
   'hlca':'Health Care Activity',
   'hops':'Hazardous or Poisonous Substance',
   'horm':'Hormone',
   'humn':'Human',
   'idcn':'Idea or Concept',
   'imft':'Immunologic Factor',
   'inbe':'Individual Behavior',
   'inch':'Inorganic Chemical',
   'inpo':'Injury or Poisoning',
   'inpr':'Intellectual Product',
   'irda':'Indicator, Reagent, or Diagnostic Aid',
   'lang':'Language',
   'lbpr':'Laboratory Procedure',
   'lbtr':'Laboratory or Test Result',
   'mamm':'Mammal',
   'mbrt':'Molecular Biology Research Technique',
   'mcha':'Machine Activity',
   'medd':'Medical Device',
   'menp':'Mental Process',
   'mnob':'Manufactured Object',
   'mobd':'Mental or Behavioral Dysfunction',
   'moft':'Molecular Function',
   'mosq':'Molecular Sequence',
   'neop':'Neoplastic Process',
   'nnon':'Nucleic Acid, Nucleoside, or Nucleotide',
   'npop':'Natural Phenomenon or Process',
   'nusq':'Nucleotide Sequence',
   'ocac':'Occupational Activity',
   'ocdi':'Occupation or Discipline',
   'orch':'Organic Chemical',
   'orga':'Organism Attribute',
   'orgf':'Organism Function',
   'orgm':'Organism',
   'orgt':'Organization',
   'ortf':'Organ or Tissue Function',
   'patf':'Pathologic Function',
   'phob':'Physical Object',
   'phpr':'Phenomenon or Process',
   'phsf':'Physiologic Function',
   'phsu':'Pharmacologic Substance',
   'plnt':'Plant',
   'podg':'Patient or Disabled Group',
   'popg':'Population Group',
   'prog':'Professional or Occupational Group',
   'pros':'Professional Society',
   'qlco':'Qualitative Concept',
   'qnco':'Quantitative Concept',
   'rcpt':'Receptor',
   'rept':'Reptile',
   'resa':'Research Activity',
   'resd':'Research Device',
   'rnlw':'Regulation or Law',
   'sbst':'Substance',
   #  
  # 'carb':'carb',
  # 'opco':'opco',
  # 'strd':'strd', steroids
  # 'adjuvant':'adjuvant',
   #
   'shro':'Self-help or Relief Organization',
   'socb':'Social Behavior',
   'sosy':'Sign or Symptom',
   'spco':'Spatial Concept',
   'tisu':'Tissue',
   'tmco':'Temporal Concept',
   'topp':'Therapeutic or Preventive Procedure',
   'virs':'Virus',
   'vita':'Vitamin',
   'vtbt':'Vertebrate',
}

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
    str = entity.replace(",","|").lower()
    translated = [semantic_types[t] if t in semantic_types else t for t in set(str.split('|')[2:])]
    return translated 

def get_image_planar(edge_list):
    buf = io.BytesIO()
    image  = nx.MultiDiGraph(edge_list)
    nx.draw_planar(image,with_labels=True)
    plt.margins(x=0.3)
    plt.savefig(buf,format='svg',transparent=True) 
    image_bytes = buf.getvalue().decode('utf-8')
    buf.close()
    plt.close()
    return image_bytes

def get_image(edge_list):
    buf = io.BytesIO()
    image  = nx.MultiDiGraph(edge_list,data=True)
    nx.draw(image,with_labels=True)
    plt.margins(x=0.3)
    plt.savefig(buf,format='svg',transparent=True) 
    image_bytes = buf.getvalue().decode('utf-8')
    buf.close()
    plt.close()
    return image_bytes


def get_entity_data(G, entity):
    return G.nodes[entity]['types']


def create_graph():
    G = nx.MultiDiGraph()

    colA = [d['entityA'].upper() for d in Triple.objects.values('entityA')] 
    colB = [d['relation'] for d in Triple.objects.values('relation')] 
    colC = [d['entityB'].upper() for d in Triple.objects.values('entityB')] 
          
    entA = fix_names(colA)
    entB = fix_names(colC)

    # add nodes first to add node attribs
    for data in range(len(entA)):
        G.add_node(entA[data],types=get_semantic_types(colA[data])) 
        G.add_node(entB[data],types=get_semantic_types(colC[data])) 

    for data in range(len(entA)):
        G.add_edge(entA[data],entB[data],relation=colB[data])

    return G

