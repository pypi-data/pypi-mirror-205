A dictionary utility of self dev py library

## Build
```shell
rm -fr dist
python -m build
# automate by following `-u {user} -p {token / password}`
# api automate by following `-u __token__ -p {token / password}`
python -m twine upload dist/*
```


```shell
PYTHONPATH=src python src/xh_py_project_versioning/__main__.py --project-file pyproject.toml --major -d
```
