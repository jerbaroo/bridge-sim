sphinx-apidoc -o sphinx-docs/source/ code/model code/**/test_*.py
cd sphinx-docs
make clean
make html
