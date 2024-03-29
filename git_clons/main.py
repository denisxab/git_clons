from os import path
import pathlib

from click import Path, argument, command, group, option

from logic import getconf_, sync_, cmd_, getlog_


@group()
def main_group():
    """
    Менеджер файлов конфигурации
    """
    ...


@command(help="Получить пути к лог файлам")
def getlog():
    getlog_()


@command(help="Получить все ссылки репозиториев у указанного пользователя")
@argument("user_name", nargs=1, type=str)
@option(
    'outfile', "-o", "--outfile",
    type=Path(dir_okay=False),
    default="./gitconf.json",
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
def getconf(user_name: str, outfile: str, token: str):
    getconf_(user_name, outfile, token)


@command(help="Синхронизироваться с gitconf.json")
@argument("path_conf", default="./gitconf.json", nargs=1, type=Path(exists=True, dir_okay=False))
@option(
    'outdir', "-o", "--outdir",
    type=Path(dir_okay=True, file_okay=False, exists=True),
    default=None,
    show_default="Там же где запущена команда",
    help="Путь для клонирования",
)
def sync(path_conf: str, outdir: str):
    sync_(path_conf, pathlib.Path(path.dirname(path_conf)) if outdir is None else outdir)


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
    cmd_(command, indir)


# @command(help="Сжать репозитории")
# @option(
#     'indir', "-i", "--indir",
#     type=Path(dir_okay=True, file_okay=False, exists=True),
#     default="./",
#     show_default="Там же где запущена команда",
#     help="Путь до локального хранения репозиториев",
# )
# @option(
#     'outpathzip', "-o", "--outpathzip",
#     type=Path(dir_okay=False),
#     default=None,
#     show_default="Там же где ``indir``",
#     help="Путь для сохранения архива",
# )
# def zip(outpathzip: str, indir: str):
#    zip_(outpathzip, indir)


# Добавляем в группу команду
main_group.add_command(getconf)
main_group.add_command(cmd)
main_group.add_command(sync)
# main_group.add_command(zip)
main_group.add_command(getlog)

if __name__ == '__main__':
    main_group()
