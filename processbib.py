"""
Copyright Sunao Sugiyama
"""

import bibtexparser # https://bibtexparser.readthedocs.io/en/master/
import os

myname1 = 'Sugiyama'
myname2 = 'Sunao'

def load_bib(fname):
    with open(fname) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database

def dump_bib(fname, bib):
    with open(fname, 'w') as f:
        bibtexparser.dump(bib, f)

def emphasize_myname(bib):
    for i, entry in enumerate(bib.entries):
        if '\myname' in entry['author']:
            continue
        bib.entries[i]['author'] = entry['author'].replace('{%s}, %s'%(myname1, myname2), '\myname{{%s}, %s}'%(myname1, myname2))
    return bib

def add_contribution(bib):
    for i, entry in enumerate(bib.entries):
        if 'contribution' in entry:
            continue
        print(f"title {entry['title']}")
        c = input(f'Major contribution? (y/n, default=y)') or 'y'
        bib.entries[i]['contribution'] = 'major' if c == 'y' else 'minor'
    return bib

def add_alphabetical(bib):
    for i, entry in enumerate(bib.entries):
        if 'alphabetical' in entry:
            continue
        print(f"title {entry['title']}")
        c = input(f'Alphabetical order? (y/n, default=n)') or 'n'
        bib.entries[i]['alphabetical'] = 'false' if c == 'n' else 'true'
    return bib

def merge_bibs(bib1, bib2, identifier='eprint'):
    """
    Merges two bibs. The first is the base bib, and the second is the new one.
    """

    bib1_ids = [entry[identifier] for entry in bib1.entries]

    for i, entry in enumerate(bib2.entries):
        if entry[identifier] in bib1_ids:
            continue
        print(f"New entry: {entry['title']}")
        bib1.entries.append(entry)

if __name__ == '__main__':
    # existing bib
    bib = load_bib('publists/refs.bib')
    
    # new bib file
    if os.path.exists('publists/refs2.bib'):
        print('>>> Adding bib entries from publists/refs2.bib to publists/refs.bib')
        bib2 = load_bib('publists/refs2.bib')
        merge_bibs(bib, bib2)

    # updates
    print('>>> Adding contribution to entries.')
    bib = add_contribution(bib)
    print('>>> Adding alphabetical or not to entries.')
    bib = add_alphabetical(bib)
    bib = emphasize_myname(bib)

    # write
    dump_bib('publists/refs.bib', bib)
