my parser

https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

create Package:
sudo rm -rf dist/
python setup.py check
python setup.py sdist
python setup.py bdist_wheel --universal

upload:
twine upload dist/\*

TODO:
https://blog.dennisokeeffe.com/blog/2021-08-11-automating-pip-package-deployment-with-github-actions
