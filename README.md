## Bibtex
1. Run custom bib
2. Then edit bst file to include adsurl (see https://github.com/yangcht/AA-bibstyle-with-hyperlink/blob/master/aa_url.bst).

## Publication list
1. Go to NASA [ADS](https://ui.adsabs.harvard.edu/search/filter_author_facet_hier_fq_author=AND&filter_author_facet_hier_fq_author=author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22&fq=%7B!type%3Daqp%20v%3D%24fq_author%7D&fq_author=(author_facet_hier%3A%221%2FSugiyama%2C%20S%2FSugiyama%2C%20Sunao%22)&q=pubdate%3A%5B2001-01%20TO%209999-12%5D%20author%3A(%22Sugiyama%2CSunao%22)&sort=date%20desc%2C%20bibcode%20desc&p_=0)
2. Export the list to a bibtex file.
3. Edit the bib file: add contribution and alphabetical attributes.
4. Run `python make_publicationlist.py`, then `publicationlist.tex` is generated.

## Talk list
1. Add talks to `talklist.xlsx`
2. Run `python make_talklist.py`, then `talklist.tex` is generated.
