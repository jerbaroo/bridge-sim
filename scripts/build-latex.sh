#!/bin/bash

cd $1

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
    rm *.out
    rm *.tex
    rm *.toc
    rm *.run.xml
}

xe $2
bibtex $2
xe $2
xe $2
rm_byproducts
