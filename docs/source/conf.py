# Файл конфигурации для конструктора документации Sphinx.
#
# Этот файл содержит только выбор наиболее распространенных опций. Для получения полного
# список см. в документации:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# Если расширения (или модули для документирования с помощью autodoc) находятся в другом каталоге,
# добавьте эти каталоги в sys.path здесь. Если каталог является относительным по отношению к
# корня документации, используйте os.path.abspath, чтобы сделать его абсолютным, как показано здесь.

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

print(sys.path)
# Путь к проекту ./../..
sys.path.insert(0, str(absolute_path_dir(__file__, 3) / "git_clons"))

print(sys.path)

# -- Project information -----------------------------------------------------

project = 'git-clones'
copyright = '2022, Denis Kustov'
author = 'Denis Kustov'

# Полная версия, включая теги alpha/beta/rc
release = '0.0.1'

# -- General configuration ---------------------------------------------------

# Добавьте сюда имена любых модулей расширения Sphinx в виде строк. Это могут быть
# расширениями, поставляемыми с Sphinx (с именем 'sphinx.ext.*') или вашими собственными
# расширения.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx.ext.intersphinx',
              "m2r2",
              ]

source_suffix = [".rst", ".md"]

# Добавьте сюда все пути, содержащие шаблоны, относительно этой директории.
templates_path = ['_templates']

# Язык для содержимого, автогенерируемого Sphinx. Обратитесь к документации
# для списка поддерживаемых языков.
# Этот параметр также используется, если вы выполняете перевод содержимого через каталоги gettext.
# Обычно для таких случаев вы задаете "language" из командной строки.
language = 'ru'

# Список шаблонов, относительно исходного каталога, которые соответствуют файлам и
# каталогов, которые следует игнорировать при поиске исходных файлов.
# Этот шаблон также влияет на html_static_path и html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# Тема, используемая для страниц HTML и HTML-справки.  См. документацию для
# список встроенных тем.
html_theme = 'sphinx_rtd_theme'

# Добавьте сюда все пути, содержащие пользовательские статические файлы (например, таблицы стилей),
# относительно этого каталога. Они копируются после встроенных статических файлов,
# поэтому файл с именем "default.css" будет перезаписывать встроенный "default.css".
html_static_path = ['_static']
