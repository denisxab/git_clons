proj_name = "gitclones.bin"

# Генерировать документацию
auto_doc:
	sphinx-autobuild -b html ./docs/source ./docs/build/html

# Создать файл зависимостей для Read The Docs
req:
	poetry export -f requirements.txt --output ./mg_file/docs/requirements.txt --dev --without-hashes;

# Скомпилировать проект
compile:
	python -m nuitka --follow-imports main.py -o $(proj_name) && mv $(proj_name) ..

debug:
	python -m nuitka main.py --follow-imports -o $(proj_name) --remove-output

