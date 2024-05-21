cd ..
python setup.py clean --all
python setup.py sdist bdist_wheel
pip install --upgrade --force-reinstall dist/icare_nlp-0.1-py3-none-any.whl
