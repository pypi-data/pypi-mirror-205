# makasuipatch
A patch to simple pro to make you activate it. Just used for learning.

## Install
```
pip install makasuipatch
```

## How to use
open `settings.py`
```
INSTALLED_APPS = [
    "simplepro",
    "simpleui",
    "import_export",
    "makasuipatch",
    ...
```

## issue
Tested compatible versions
```
- 6.x
```

## Package command
```
# build
python -m build

# upload to testpypi repo 
twine upload --repository testpypi dist/*

# install from testpypi repo 
pip install -i https://test.pypi.org/simple/ --no-deps makasuipatch

# upload to product repo
twine upload dist/*

# install from testpypi repo 
pip install makasuipatch --no-cache-dir
```
