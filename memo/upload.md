# update version

modify '__version__' in '__init__.py'

# build

```shell
pip install twine
pip install wheel

python3 setup.py sdist
python3 setup.py bdist_wheel
```

# setup
create ~/.pypirc

```txt:.pypirc
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: [name]
password: [pass]

[testpypi]
repository: https://test.pypi.org/legacy/
username: [name]
password: [pass]
```

# upload test site
```shell
twine upload --repository testpypi dist/*
```

# upload pypi site
```shell
twine upload --repository pypi dist/*
```

# install

```shell
pip install --index-url https://test.pypi.org/simple/ [パッケージ名]
```

# referrence
[referrence](https://qiita.com/c60evaporator/items/e1ecccab07a607487dcf)
