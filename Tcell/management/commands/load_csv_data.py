from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from Tcell.models import Epitope

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Epitope.objects.exists():
            print('Epitope data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading Epitope data")

        # Code to load the data into database
        for row in DictReader(open('./data/FINAL.csv')):
            epitope = Epitope(
                key = row['key'],

                sequence=row['Epitope sequence'],
                mhc_ambiguity=row['MHC Ambiguity'],
                old_allele_name=row['Old allele name'],
                mhc_convert=row['MHC Convert'],
                mhc_possible=row['MHC Possible'],
                pmid=row['PMID'],
                date=row['Date'],
                title=row['Title'],
                journal=row['Journal'],
                authors=row['Authors'],
                tcellid=row['T Cell ID'],
                sourcemolecule=row['Epitope Source Molecule'],
                sourceorganism=row['Epitope Source Organism'],
                epitopespecies=row['Epitope Species'],
                method=row['Method'],
                Response=row['Response measured'],
                qualitative=row['Qualitative Measurement'],
                quantitative=row['Quantitative measurement'],
                gene=row['Epitope gene'],
                dbsource=row['Database source'],

                pdbclear=row['pdb_clear'],
                pdbamb=row['pdb_amb'],
                pdbid=row['pdbid'],
                bound=row['bound'],
                pdb_pmid = row['pdb_pmid'],
                pdb_date=row['release_date'],
                VA_Chain=row['VA chain'],
                VB_Chain=row['VB chain'],
                VA_IMGT=row['VA IMGT details'],
                VB_IMGT=row['VB IMGT details'],
                Ag_Chain=row['Antigen Chain'],
                MHC_Chain=row['MHC_chains'],
            )
            epitope.save()
