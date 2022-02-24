proj_name = "git_clons"
name_bin_file = "gitclones.bin"

# Генерировать документацию
auto_doc:
	sphinx-autobuild -b html ./docs/source ./docs/build/html

# Создать файл зависимостей для Read The Docs
req_doc:
	poetry export -f requirements.txt --output ./docs/requirements.txt --dev --without-hashes;

# Скомпилировать проект
compile:
	python -m nuitka --follow-imports $(proj_name)/main.py -o $(name_bin_file)

debug:
	python -m nuitka --follow-imports $(proj_name)/main.py -o $(name_bin_file) --remove-output

