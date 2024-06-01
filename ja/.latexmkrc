#!/usr/bin/perl

# For handling Japanese documents with uplatex and dvipdfmx
$latex     = 'uplatex %O -synctex=1 %S';
$pdflatex  = 'pdflatex %O -synctex=1 %S';
$biber     = 'biber %O -u -U --output_safechars %B';
$bibtex    = 'pbibtex %O %B';
$dvipdf    = 'dvipdfmx %O -o %D %S';
$makeindex = 'mendex %O -o %D %S';
$pdf_mode  = 4; # .tex -> .dvi -> .pdf

# Ensure that all the required steps are run
add_cus_dep('glo', 'gls', 0, 'makeindex');
add_cus_dep('nlo', 'nls', 0, 'makeindex');
add_cus_dep('acn', 'acr', 0, 'makeindex');
