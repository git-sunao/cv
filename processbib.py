"""
Copyright Sunao Sugiyama
"""

import bibtexparser # https://bibtexparser.readthedocs.io/en/master/
import numpy as np

def load_bib(fname):
    with open(fname) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database

def dump_bib(fname, bib):
    with open(fname, 'w') as f:
        bibtexparser.dump(bib, f)

def emphasize_myname(bib):
    for i in range(len(bib.entries)):
        if '\myname' in bib.entries[i]['author']:
            continue
        bib.entries[i]['author'] = bib.entries[i]['author'].replace('{Sugiyama}, Sunao', '\myname{{Sugiyama}, Sunao}')
    return bib

if __name__ == '__main__':
   bib = load_bib('refs.bib')
   bib = emphasize_myname(bib)
   dump_bib('refs.bib', bib)
