from os import path, makedirs, listdir
from time import time
from typing import Optional

from logsmal import loglevel, logger
from mg_file.file.json_file import JsonFile
from mg_file.file.zip_file import ZippFile
from mg_file.pcos.base_pcos import os_exe_thread

from pars_git import ParseGit

PATH_INFO_LOG = "./log/info.log"
PATH_ERROR_LOG = "./log/error.log"

logger.info = loglevel(
    "[INFO]",
    PATH_INFO_LOG,
    console_out=True,
    max_size_file="1mb"
)
logger.error = loglevel(
    "[ERROR]",
    PATH_ERROR_LOG,
    console_out=True,
    max_size_file="1mb",
)


def getrep_(user_name: str, outfile: str, token: str):
    """
    Получить данные с сервера ``GitHub``, по умолчанию данные сохранятся
    в файл ``./look.json``

    :param user_name: Имя пользователя GitHub
    :param outfile: Куда поместить файл с результатом
    :param token: Токен пользователя GitHub *пока не используется в логики программы*


    :Пример запуска:

    .. code-block:: text

        python main.py getrep denisxab -o /home/denis/prog/GIT/look.json


    .. note::

        Можно вручную добавлять репозитории в конфигурацию ``look.json``.
        Вот структура для храня ``look.json`` :meth:`pars_git.Tall_repos`

        :Пример ручного добавления репозитория:

        .. code-block:: json

            "all_repos": {
                ...,
                  "ИмяПроекта": {
                    "visibility": "private",
                    "clone_url": "https://USERNAME:TOKEN@github.com/denisxab/ИмяПроекта.git",
                    "default_branch": "master"
                }
                ...,
            }

    """
    #: Получить данные из существующей конфигурации
    data_in_file = JsonFile(outfile).readFile()
    res = ParseGit(user_name=user_name, token=token)
    if data_in_file:
        res['all_repos'].update(data_in_file['all_repos'])
    # Записать данные в файл
    JsonFile(outfile).writeFile(res, sort_keys=False)
    print("END")


def clones_(path_look: str, outdir: str):
    """
    Клонировать репозитории

    :param path_look: Путь к файлу с настройками
    :param outdir: Куда клонировать репозитории

    :Пример запуска:

    .. code-block:: text

        python main.py clones -o /home/denis/prog/GIT/
    """
    command_list: list[str] = []
    res: dict = JsonFile(path_look).readFile()
    for _name_rep, _val_rep in res["all_repos"].items():
        command_list.append(f"git clone {_val_rep['clone_url']} {path.join(outdir, _name_rep)}")

    os_exe_thread("CLONE", command_list, call_log_info=logger.info, call_log_error=logger.error)


def cmd_(command: str, indir: str, ):
    """
    Выполнить команду в каждом репозитории

    :param command: Команда
    :param indir: Путь к папке с репозиториями

    :Пример запуска Обновить все репозитории:

    .. code-block:: text

        python main.py cmd pull -i /home/denis/prog/GIT/
    """

    command_list: list[str] = []
    for _path in listdir(indir):
        if path.isdir(path.join(indir, _path)):
            command_list.append(f"cd {path.join(indir, _path)} && git {command}")

    os_exe_thread(command, command_list, call_log_info=logger.info, call_log_error=logger.error)


def zip_(outpathzip: Optional[str], indir: str):
    """
    Архивировать репозитории

    :param outpathzip: Куда сохранить архив. По умолчанию там же где
        ``indir`` в папке `zip/git_zip{время}.zip`
    :param indir: Путь к папке с репозиториями


    :Пример запуска:

    .. code-block:: text

        python main.py zip -i /home/denis/prog/GIT/
    """
    if outpathzip is None:
        makedirs(f"{indir}/zip", exist_ok=True)
        outpathzip = f"{indir}/zip/git_zip{int(time())}.zip"

    ZippFile(outpathzip,call_log_info=logger.info,call_log_error=logger.error).writePath(
        indir,
        # Исключим папку в которой находятся архивы
        execute_path={"zip"}
    )


def getlog_():
    """
    Получить пути к лог файлам
    """
    print(f"info: {path.abspath(PATH_INFO_LOG)}\nerror: {path.abspath(PATH_ERROR_LOG)}\n")
