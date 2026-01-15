import argparse
import os
from typing import Tuple, Union, Any, Dict

import pandas as pd
from pandas import Series, DataFrame
from pandas.core.generic import NDFrame

from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')
out_columns = ["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart",
               "qend", "sstart", "send", "eval", "bitscore", "qlen", "slen", "Database source"]


def prepare_databaseDF():
    db_path = f"./DB/Pathgeon.csv"
    print(f'Reading .... {db_path}')
    Ref_df = pd.read_csv(db_path)
    return Ref_df


def gen_fasta() -> str:
    """
    Generate fasta with test peptide,
    only with one sequence,
    no return but one "test.fasta"
    str: test_peptide:
    return:
        None
    """
    fasta_name = "test.fasta"
    fasta_f = open(fasta_name, 'w')
    print(f">test\n{peptide}", file=fasta_f)  # header of peptide
    fasta_f.close()
    fastafilepath = os.path.abspath(fasta_name)
    print(f'Generating....... {fasta_name}')
    return fastafilepath


def run_blast(fasta_file_path):
    basename = os.path.basename(fasta_file_path)
    fasta_fname = os.path.splitext(basename)[0]
    out_path = f"{fasta_fname}.out"
    Command = f'blastp -db ./DB/Pathgeon -query {fasta_file_path} -out {out_path} -num_threads 5 -evalue 10 -outfmt "6 std qlen slen"'
    print(f'Processing.......\n {Command}')
    # TODO 記得把這裡碼掉
    os.system(Command)
    print('......Done.......')
    return out_path

def BlastOut_Distillate(out_path) -> tuple[Any, dict[Any, Any]]:
    print(f'Distillating {out_path} ')
    df = pd.read_csv(f"{out_path}",
                     sep='\t',
                     names=out_columns)
    # 100% Matched
    # 0502 qlen == slen
    # Matched = df[(df['pident'] == pid) & (df['length'] == df['slen']) & (df['qlen'] == df['slen'])]
    if pid == 100:
        Matched = df[
            (df['pident'] == pid) & (df['length'] == df['slen']) & (df['qlen'] == df['slen']) & (df['gapopen'] == gap) & (
                    df['mismatch'] == sub)]
    else:
        Matched = df[(df['pident'] != 100) & (df['pident'] >= pid) & (df['length'] == df['slen']) & (df['qlen'] == df['slen'])]
    Matched['status'] = 'Matched'
    Final_df = Matched
    print(Final_df.columns)
    print(Final_df)
    Matched_List = {}
    for key, item in tqdm(Final_df.groupby('qseqid')):
        item = item.dropna(subset=['sseqid'])
        Matched_List[peptide] = pd.DataFrame({
            'qid': str(key),
            'key': item['sseqid'],
            'blast_status': item['status'].values,
            'HLA_status': [itm.split('_')[-1] for itm in item['sseqid'].values],
            'pident': item['pident'].values,
            'length': item['length'].values,
            'qlen': item['qlen'].values,
            'mismatch': item['mismatch'].values,
            'slen': item['slen'].values,
            'query_peptide': peptide,
        }).drop_duplicates()
    return Final_df, Matched_List


def Generate_Output_list(Matched_List, Ref_df) -> list:
    Li = []
    for _, df in tqdm(Matched_List.items()):
        Li.append(df)
    frame = pd.concat(Li, axis=0, ignore_index=True)
    frame = frame.drop_duplicates()
    frame = frame.merge(Ref_df, on='key')
    #print(frame)
    return list(frame['key'].values)


def pathogen_main(test_sequence, pident=100, gap_pos=0, sub_pos=0) -> list:
    """
    str: test_peptide
    return:
        list:matched_keys
    """
    global peptide, pid, gap, sub
    peptide, pid, gap, sub = test_sequence, pident, gap_pos, sub_pos
    #print('test',peptide,pid)
    Ref_df = prepare_databaseDF()
    fasta_path = gen_fasta()
    out_path = run_blast(fasta_path)
    Final_df, Matched_List = BlastOut_Distillate(out_path)
    #print(Matched_List)
    if not Matched_List:
        return []
    key_list = Generate_Output_list(Matched_List, Ref_df)
    return key_list


#key_list = pathogen_main('NSELIRRAKAAESLASD')
#print(key_list)
