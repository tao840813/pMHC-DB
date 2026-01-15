# Create your views here.
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from Tcell.models import Epitope
from django.templatetags.static import static

from Pathogen_similarity.Pathogen_single import pathogen_main
from Pathogen_similarity.reference_table import Reference_Table

from Tcell.pdb_process import Seq_dict,SearchPos

# Create your views here.
def home(request):
    return HttpResponse("Home page")


def index(request):
    check_strings = request.GET.get('peptide')
    mhc_ambiguity = request.GET.get('ambiguity')
    epitope_species = request.GET.get('species')
    select_assay = request.GET.get('assay')

    Similarity_Btn = request.GET.get('pathogen')
    epitopes = Epitope.objects.all()
    if mhc_ambiguity:
        epitopes = epitopes.filter(mhc_ambiguity=mhc_ambiguity)
    if epitope_species:
        epitopes = epitopes.filter(epitopespecies=epitope_species)
    if select_assay:
        epitopes = epitopes.filter(method__in=Reference_Table[select_assay])

    if Similarity_Btn == 'pathogen':
        key_list = pathogen_main(check_strings)
        print(key_list)
        epitopes = Epitope.objects.filter(key__in=key_list)

    if Similarity_Btn == 'self':
        print('not done yet')
    # print('select_assay',select_assay,Reference_Table[select_assay])

    per_page = 10
    paginator = Paginator(epitopes, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pmids = epitopes.values('pmid', 'title', 'date', 'journal', 'method').distinct()


    context = {
        'pmids': pmids,
        'page_obj': page_obj,
        'ambiguity_choices': Epitope.objects.values_list('mhc_ambiguity', flat=True).distinct(),
        'species_choices': sorted(Epitope.objects.values_list('epitopespecies', flat=True).distinct()),
        'assay_choices': ["3D", "Binding Activity", "Cytokine release", "Binding"],
        'selected_ambiguity': mhc_ambiguity,
        'selected_species': epitope_species,
        'selected_assay': select_assay,
        'total_pmid': len(pmids),
        'total_epitopes': len(epitopes)
    }
    return render(request, 'index.html', context)


def pmid_detail(request, pk):
    """
    <td><a href="{% url 'pmid_detail' pk=pmid.pmid %}" class="pmid-link">{{ pmid.pmid }}</a></td>
    """
    epitopes = Epitope.objects.all()
    epitopes = epitopes.filter(pmid=pk)
    context = {
        'epitopes': epitopes,
    }
    return render(request, 'pmid.html', context)


def assay_detail(request, pk):
    epitopes = Epitope.objects.all()
    epitopes = epitopes.filter(key=pk)
    context = {
        'epitope': epitopes,
    }

    first_epitope = epitopes[0]
    template_name = 'assay_pic.html'
    if first_epitope.pdbid and first_epitope.Ag_Chain:
        template_name = 'assay_pdb.html'
        pdb_url = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'PDB', f'{first_epitope.pdbid}.pdb')
        Seqs = Seq_dict(pdb_url)
        if '|' in first_epitope.Ag_Chain:
                first_epitope.Ag_Chain = first_epitope.Ag_Chain[0]
        Ag_seq = Seqs[first_epitope.Ag_Chain]
        #MHC通常會有兩條chain
        MHC_chain1,MHC_chain2 = first_epitope.MHC_Chain.split('|')
        MHC_chain1, MHC_chain2 = MHC_chain1.strip(), MHC_chain2.strip()
        MHC_seq1, MHC_seq2 = Seqs[MHC_chain1], Seqs[MHC_chain2]
        #TCR
        TCR_VA_seq, TCR_VB_seq = Seqs[first_epitope.VA_Chain], Seqs[first_epitope.VB_Chain]
        #print(Ag_seq)
        key_list = pathogen_main(Ag_seq,pident=80)
            #print(key_list)
        alike_epitopes = Epitope.objects.all()
        alike_epitopes = Epitope.objects.filter(key__in=key_list)
        context = {
                'epitope': first_epitope,
                'pdbfile':first_epitope.pdbid+'.pdb',
                'epitope_chain':first_epitope.Ag_Chain,
                'epitope_peptide':Ag_seq,
                'MHC_Chain1':MHC_chain1,
                'MHC_seq1':MHC_seq1,
                'MHC_Chain2': MHC_chain2,
                'MHC_seq2': MHC_seq2,
                'TCR_VA_Chain': first_epitope.VA_Chain,
                'TCR_VA_seq': TCR_VA_seq,
                'TCR_VB_Chain': first_epitope.VB_Chain,
                'TCR_VB_seq': TCR_VB_seq,
                'alike_epitopes':alike_epitopes,
                'command':f';spin on;spacefill; \
                             select :{first_epitope.Ag_Chain},:{first_epitope.VA_Chain},:{first_epitope.VB_Chain},:{first_epitope.MHC_Chain};restrict selected;\
                             select *;color grey;\
                             select :{first_epitope.MHC_Chain};color pink;\
                             select :{first_epitope.Ag_Chain};color red;\
                             select :{first_epitope.VA_Chain};color lightgreen;\
                             select :{first_epitope.VB_Chain};color lightblue; save STATE'\
                             ,
                'show_pMHC_Command': f'select :{first_epitope.Ag_Chain},:{first_epitope.MHC_Chain};restrict selected;',
                'show_TCR_Command': f'select :{first_epitope.VA_Chain},:{first_epitope.VB_Chain};restrict selected;',
            }
            #print('first',first_epitope.pdbid,first_epitope.Ag_Chain)


    return render(request, template_name, context)


def search(request):
    epitopes = Epitope.objects.all()

    if request.GET.get('ambiguity'):
        epitopes = epitopes.filter(mhc_ambiguity=request.GET['ambiguity'])

    context = {
        'epitopes': epitopes,
        'ambiguity_choices': Epitope.objects.values_list('mhc_ambiguity', flat=True).distinct(),
        'selected_ambiguity': request.GET.get('ambiguity', '')
    }
    return render(request, 'index_test.html', context)
