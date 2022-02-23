import os

from click import Path, argument, command, group, option

from logic import get_rep, clones_, cmd_, zip_


@group()
def main_group():
    """Менеджер файлов конфигурации"""
    ...


@command(help="Получить все ссылки репозиториев у указанного пользователя")
@argument("user_name", nargs=1, type=str)
@option(
    'outfile', "-o", "--outfile",
    type=Path(dir_okay=False),
    default="./look.json",
    show_default="Там же где запущена команда",
    help="Путь для сохранения",
)
@option(
    'token', "-t", "--token",
    type=str,
    default=None,
    show_default="Нет токена",
    help="Токен пользователя GitHub",
)
def getrep(user_name: str, outfile: str, token: str):
    """
    Получить данные с сервера ``GitHub``

    :Пример запуска:

    .. code-block:: text

        python main.py getrep denisxab
        python main.py getrep denisxab -o /home/denis/prog/GIT/look.json;

    """
    get_rep(user_name, outfile, token)


@command(help="Скачать все репозитории указанные в look.json")
@argument("path_look", default="./look.json", nargs=1, type=Path(exists=True, dir_okay=False))
@option(
    'outdir', "-o", "--outdir",
    type=Path(dir_okay=True, file_okay=False, exists=True),
    default=None,
    show_default="Там же где запущена команда",
    help="Путь для клонирования",
)
def clones(path_look: str, outdir: str):
    """
    Клонировать репозитории


    :Пример запуска:

    .. code-block:: text

        python main.py clones -o /home/denis/PycharmProjects/git_clons/git_clons/test/data_set

    """
    if outdir is None:
        outdir = os.path.dirname(path_look)

    clones_(path_look, outdir)


@command(help="Выполнить команду в каждом репозитории")
@argument("command", nargs=1)
@option(
    'indir', "-i", "--indir",
    type=Path(dir_okay=True, file_okay=False, exists=True),
    default="./",
    show_default="Там же где запущена команда",
    help="Путь до локального хранения репозиториев",
)
def cmd(command: str, indir: str):
    """
    Обновить репозитории

    :Пример запуска Обновить все репозитории:

    .. code-block:: text

        python main.py cmd pull -i /home/denis/PycharmProjects/git_clons/git_clons/test/data_set
    """
    cmd_(command, indir)


@command(help="Сжать репозитории")
@option(
    'indir', "-i", "--indir",
    type=Path(dir_okay=True, file_okay=False, exists=True),
    default="./",
    show_default="Там же где запущена команда",
    help="Путь до локального хранения репозиториев",
)
@option(
    'outpathzip', "-o", "--outpathzip",
    type=Path(dir_okay=False),
    default=None,
    show_default="Там же где ``indir``",
    help="Путь для сохранения архива",
)
def zip(outpathzip: str, indir: str):
    """
    Архивировать репозитории

    :Пример запуска:

    .. code-block:: text

        python main.py zip -i /home/denis/PycharmProjects/git_clons/git_clons/test/data_set
    """
    zip_(outpathzip, indir)


# Добавляем в группу команду
main_group.add_command(getrep)
main_group.add_command(cmd)
main_group.add_command(clones)
main_group.add_command(zip)

if __name__ == '__main__':
    main_group()
