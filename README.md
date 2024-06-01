## Main files

The tex files below can be compiled by

```console
latexmk -pdfdvi cv
```

1. [cv.tex](cv.tex) is the tex file for CV.
2. [pl.tex](pl.tex) is the tex file for publication list only.

## How to prepare bibtex for publication list

1. Run custom bib
2. Then edit bst file to include adsurl (see https://github.com/yangcht/AA-bibstyle-with-hyperlink/blob/master/aa_url.bst).

## How to make a publication list
1. Go to NASA [ADS](<https://ui.adsabs.harvard.edu/search/filter_author_facet_hier_fq_author=AND&filter_author_facet_hier_fq_author=author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22&fq=%7B!type%3Daqp%20v%3D%24fq_author%7D&fq_author=(author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22)&q=pubdate%3A%5B2001-01%20TO%209999-12%5D%20author%3A(%22Sugiyama%2CSunao%22)&sort=date%20desc%2C%20bibcode%20desc&p_=0>)
2. Export the list to a bibtex file. If this is the first time to make publication list, then save the bib file as "publists/refs.bib", otherwise, "publists/refs2.bib".
3. Run `python process.py`, then `refs.bib` is updated.
4. Run `python make_publicationlist.py`, then `publicationlist.tex` is generated.

## How to make a talk list

1. Add talks to `talklist.xlsx`
2. Run `python make_talklist.py`, then `talklist.tex` is generated.

## TODO
- link to proper documents
    - from en to jp
    - from website to cv
- add non-journal article publication
