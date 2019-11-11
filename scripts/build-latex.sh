#!/bin/bash

cd $1

xe() {
    xelatex -shell-escape -interaction=nonstopmode "$1"
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
biblatex $2
xe $2
biblatex $2
xe $2
