sphinx-apidoc -o sphinx-docs/source/ public/model public/**/test_*.py
cd sphinx-docs
make clean
make html
