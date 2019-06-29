#!/bin/bash

xe() {
    xelatex -interaction=nonstopmode "$1"
}

rm_byproducts() {
    rm *.aux
    rm *.bbl
    rm *.bcf
    rm *.blg
    rm *blx.bib
    rm *.log
    rm *.tex
    rm *.toc
    rm *.run.xml
}

xe thesis
bibtex thesis
xe thesis
xe thesis
rm_byproducts
