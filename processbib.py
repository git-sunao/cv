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

def print_bib_entry(bib_entry):
    nmax = 0
    for key, val in bib_entry.items():
        nmax = max(nmax, len(key))
    for key, val in bib_entry.items():
        print(key.ljust(nmax+5), '|', val)

def merge_bibs(bib1, bib2, identifier='eprint', update=False):
    """
    Merges two bibs. The first is the base bib, and the second is the new one.
    """

    bib1_ids = [entry[identifier] for entry in bib1.entries]

    for i, entry in enumerate(bib2.entries):
        if not identifier in entry:
            print(f"Entry {entry['title']} does not have an identifier={identifier}. Skipping.")
            continue
        if entry[identifier] in bib1_ids:
            if update:
                bib1_idx = bib1_ids.index(entry[identifier])
                entry_bib1 = bib1.entries[bib1_idx]
                for key, val in entry.items():
                    if key in entry_bib1: continue
                    entry_bib1[key] = val
                bib1.entries[bib1_idx] = entry_bib1
        else:
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
