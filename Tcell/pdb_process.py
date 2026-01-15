d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
         'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
         'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
         'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

from Bio.PDB.PDBParser import PDBParser


def Seq_dict(filename):
    p = PDBParser(PERMISSIVE=1, QUIET=True)
    structure = p.get_structure("1ppi", filename)
    model = structure[0]
    Seq_dict = {}
    for chain in model:
        seq = []
        chain_name = chain.get_id()
        for residue in chain:
            residue_name = residue.resname
            if residue_name not in d3to1:
                continue
            seq.append(d3to1[residue.resname])
        Seq_dict[chain_name] = ''.join(seq)
    return Seq_dict


def SearchPos(Seq, peptide):
    first_pos = Seq.find(peptide)
    end_pos = first_pos + len(peptide)
    return [i for i in range(first_pos, end_pos + 1)]
