#!/usr/bin/perl

$pdflatex  = 'pdflatex %O -synctex=1 %S';
$biber     = 'biber %O -u -U --output_safechars %B';
$bibtex    = 'bibtex %O %B';
$dvipdf    = 'dvipdfmx %O -o %D %S';
$makeindex = 'mendex %O -o %D %S';
$pdf_mode  = '5'; # .tex -> .dvi -> .pdf
