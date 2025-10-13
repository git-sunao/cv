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

def my_paper_publications_sorted_by_date(language='en'):
    bibd = load_bib('publists/refs.bib')
    entries_sorted = sort_entries_by_year_month(bibd)
    entries_major, entries_contributing = split_into_major_and_contributing(entries_sorted)

    def check_ab(entry):
        if entry['alphabetical'] == 'true':
            ab = '*'
        else:
            ab = ''
        return ab

    tex = ''
    if language == 'en':
        tex+= '* = Author list alphabetized\\\\\n'
        # tex+= '\\noindent\\textbf{\\textit{Major author}}\n'
        tex+= '\\noindent\\textbf{\\textit{First-author papers or co-authored papers with significant contributions}}\n'
    else:
        tex+= '* = 著者リストアルファベット順\\\\\n'
        # tex+= '\\noindent\\textbf{\\textit{主著者}}\n'
        tex+= '\\noindent\\textbf{\\textit{筆頭著者または主要な貢献をした査読付論文}}\n'

    tex+= '\\begin{enumerate}\n'
    for entry in entries_major:
        tex+= "\\item " + check_ab(entry) + "\\bibentry{%s}"%entry['ID']
        if 'status' in entry:
            tex += ', %s'%entry['status']
        tex += '\n'
    tex+= '\\end{enumerate}\n'
    tex+= '\n'

    if len(entries_contributing) > 0:
        # tex+= '\\noindent\\textbf{\\textit{Contributing author}}\n' if language == 'en' else '\\noindent\\textbf{\\textit{共著者}}\n'
        tex+= '\\noindent\\textbf{\\textit{co-authored  papers}}\n' if language == 'en' else '\\noindent\\textbf{\\textit{その他の共著論文}}\n'
        tex+= '\\begin{enumerate}\n'
        tex+= '\\setcounter{enumi}{%d}'%len(entries_major)
        for entry in entries_contributing:
            tex+= "\\item " + check_ab(entry) + "\\bibentry{%s}"%entry['ID']
            if 'status' in entry:
                tex += ', %s'%entry['status']
            tex += '\n'
        tex+= '\\end{enumerate}\n\n'

    return tex

def my_article_sorted_by_date(language='en'):
    bibd = load_bib('publists/article.bib')
    entries_sorted = sort_entries_by_year_month(bibd)
    tex = ''
    if language == 'en':
        tex+= '\\noindent\\textbf{\\textit{Other Articles}}\n'
    else:
        tex+= '\\noindent\\textbf{\\textit{他の記事}}\n'

    tex+= '\\begin{enumerate}\n'
    for entry in entries_sorted:
        tex+= "\\item \\bibentry{%s}"%entry['ID']
        if 'status' in entry:
            tex += ', %s'%entry['status']
        tex += '\n'
    tex+= '\\end{enumerate}\n'
    tex+= '\n'

    return tex

def wrap_cv_style(tex_in, language='en', fullauthor=False):

    if language == 'en':
        tex = '\\begin{rSection}{PUBLICATIONS}\n'
        tex+= 'The up-to-date list of publication availabele at \\href{https://ui.adsabs.harvard.edu/search/filter_author_facet_hier_fq_author=AND&filter_author_facet_hier_fq_author=author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22&fq=%7B!type%3Daqp%20v%3D%24fq_author%7D&fq_author=(author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22)&q=pubdate%3A%5B2001-01%20TO%209999-12%5D%20author%3A(%22Sugiyama%2CSunao%22)&sort=date%20desc%2C%20bibcode%20desc&p_=0}{ADS}.\n'
        tex+= '\\vspace{-53em}\n'
        tex+= '\\nobibliography{../publists/refs, ../publists/article}\n'
    else:
        tex = '\\begin{rSection}{出版/発表論文}\n'
        tex+= '最新の論文リストは\\href{https://ui.adsabs.harvard.edu/search/filter_author_facet_hier_fq_author=AND&filter_author_facet_hier_fq_author=author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22&fq=%7B!type%3Daqp%20v%3D%24fq_author%7D&fq_author=(author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22)&q=pubdate%3A%5B2001-01%20TO%209999-12%5D%20author%3A(%22Sugiyama%2CSunao%22)&sort=date%20desc%2C%20bibcode%20desc&p_=0}{ADS}を参照ください。'
        tex+= '\\vspace{-53em}\n'
        tex+= '\\nobibliography{../publists/refs, ../publists/article}\n'

    tex+= tex_in

    if fullauthor:
        tex+= '\\bibliographystyle{../sty/fullauthor}'
    else:
        tex+= '\\bibliographystyle{../sty/etalstyle}'
    tex+= '\\end{rSection}\n'

    return tex

if __name__ == '__main__':
    for language in ['en', 'ja']:
        tex = my_paper_publications_sorted_by_date(language=language)
        tex+= my_article_sorted_by_date(language=language)
        tex = wrap_cv_style(tex, language=language)
        fname_out='{}/publist.tex'.format(language)
        with open(fname_out, 'w') as f:
            print('writing to {}'.format(fname_out))
            f.write(tex)

    for language in ['en', 'ja']:
        tex = my_paper_publications_sorted_by_date(language=language)
        tex+= my_article_sorted_by_date(language=language)
        tex = wrap_cv_style(tex, language=language, fullauthor=True)
        fname_out='{}/publist_fullauthor.tex'.format(language)
        with open(fname_out, 'w') as f:
            print('writing to {}'.format(fname_out))
            f.write(tex)
