# build

```shell
pip install twine
pip install wheel

python setup.py sdist
python setup.py bdist_wheel
```

# setup
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

# upload
```shell
twine upload --repository testpypi dist/*
twine upload --repository pypi dist/*
```

# install

```shell
pip install --index-url https://test.pypi.org/simple/ [パッケージ名]
```

# referrence
[referrence](https://qiita.com/c60evaporator/items/e1ecccab07a607487dcf)
