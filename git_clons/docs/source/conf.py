import os
import sys
from pathlib import Path


def absolute_path_dir(_file: str, back: int = 1) -> Path:
    """
    Получить абсолютный путь к своей директории

    :param _file: Путь
    :param back: Сколько отступить назад
    """
    res = Path(_file).resolve()
    for _ in range(back):
        res = res.parent
    return res


sys.path.insert(0, os.path.abspath('.'))

# Путь к проекту ./../..
sys.path.insert(0, str(absolute_path_dir(__file__, 3)))
print(sys.path)

project = 'git_clons'
copyright = '2022, Denis Kustov'
author = 'Denis Kustov'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx.ext.intersphinx',
              "m2r2",
              ]
source_suffix = [".rst", ".md"]
templates_path = ['_templates']
language = 'ru'
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
