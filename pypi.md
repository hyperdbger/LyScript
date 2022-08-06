python -m pip install --user --upgrade setuptools wheel
python -m pip install --user --upgrade twine

python setup.py sdist bdist_wheel

python -m twine upload dist/*
