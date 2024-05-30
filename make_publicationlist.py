"""
Copyright Sunao Sugiyama

How to use.
1. prepare a bib file (see readme to extract your bib from NANA/ADS)
2. edit the bib file
    - add two items to every entry: contribution and alphabetical
    - replace your name with emphasized name: use `processbib.py`
3. run this script, then ``publist/publist.tex'' is generated auto matically.
"""

import bibtexparser # https://bibtexparser.readthedocs.io/en/master/
import numpy as np

def load_bib(fname):
    with open(fname) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database

def sort_entries_by_year_month(bib_database):
    entries = bib_database.entries

    dates = []
    for entry in entries:
        month = {'January'  :'01',
                 'February' :'02',
                 'March'    :'03',
                 'April'    :'04',
                 'May'      :'05',
                 'June'     :'06',
                 'July'     :'07',
                 'August'   :'08',
                 'September':'09',
                 'October'  :'10',
                 'November' :'11',
                 'December' :'12'}[entry['month']]
        date = entry['year'] + '-' + month
        dates.append(date)   

    idx = np.argsort(dates)
    
    entries_sorted= [entries[i] for i in idx[::-1]]
    return entries_sorted 

def split_into_major_and_contributing(entries):
    major = []
    contributing = []
    for entry in entries:
        if entry['contribution'] == 'major':
            major.append(entry)
        elif entry['contribution'] == 'contributing' or entry['contribution'] == 'minor':
            contributing.append(entry)
    return major, contributing

def my_paper_publications_sorted_by_date():
    bibd = load_bib('publists/refs.bib')
    entries_sorted = sort_entries_by_year_month(bibd)
    entries_major, entries_contributing = split_into_major_and_contributing(entries_sorted)

    def check_ab(entry):
        if entry['alphabetical'] == 'true':
            ab = '*'
        else:
            ab = ''
        return ab

    tex = '* = Author list alphabetized\\\\\n'
    tex+= '\\noindent\\textbf{\\textit{Major author}}\n'
    tex+= '\\begin{enumerate}\n'
    for entry in entries_major:
        tex+= "\\item " + check_ab(entry) + "\\bibentry{%s}"%entry['ID']
        if 'status' in entry:
            tex += ', %s'%entry['status']
        tex += '\n'
    tex+= '\\end{enumerate}\n'
    tex+= '\n'

    if len(entries_contributing) > 0:
        tex+= '\\noindent\\textbf{\\textit{Contributing author}}\n'
        tex+= '\\begin{enumerate}\n'
        tex+= '\\setcounter{enumi}{%d}'%len(entries_major)
        for entry in entries_contributing:
            tex+= "\\item " + check_ab(entry) + "\\bibentry{%s}"%entry['ID']
            if 'status' in entry:
                tex += ', %s'%entry['status']
            tex += '\n'
        tex+= '\\end{enumerate}'

    with open('publists/publist.tex', 'w') as f:
        f.write(tex)


if __name__ == '__main__':
   my_paper_publications_sorted_by_date() 
