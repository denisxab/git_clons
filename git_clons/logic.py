from os import path, makedirs, listdir
from time import time
from typing import Optional

from logsmal import logger
from mg_file.file.json_file import JsonFile
from mg_file.file.zip_file import ZippFile
from mg_file.pcos.base_pcos import os_exe_async, type_os_res

from pars_git import ParseGit, TypeRepos
import jmespath

PATH_INFO_LOG = "./log/info.log"
PATH_ERROR_LOG = "./log/error.log"

logger.info.fileout = PATH_INFO_LOG
logger.error.fileout = PATH_ERROR_LOG


def getrep_(user_name: str, outfile: str, token: str):
    """
    Получить данные с сервера ``GitHub``, по умолчанию данные сохранятся
    в файл ``./look.json``

    :param user_name: Имя пользователя GitHub
    :param outfile: Куда поместить файл с результатом
    :param token: Токен пользователя GitHub *пока не используется в логики программы*

    """
    #: Получить данные из существующей конфигурации
    data_in_file = JsonFile(outfile).readFile()
    res = ParseGit(user_name=user_name, token=token)
    if data_in_file:
        # Переносим закрытые репозитории из текущего файла. И обновляем токен из URL на тот который мы передали 
        res['all_repos'].update(
            {
                k: v for k, v in data_in_file['all_repos'].items()
                if v['visibility'] == TypeRepos.private.value
            }
        )
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
        command_list.append(
            f"git clone {_val_rep['clone_url']} {path.join(outdir, _name_rep)}")

    res: list[type_os_res] = os_exe_async(command_list=command_list)
    for _x in res:
        _x.__str__(logger_info=logger.info,
                   logger_error=logger.error, flag="CLONES")


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
            command_list.append(
                f"cd {path.join(indir, _path)} && git {command}")

    res: list[type_os_res] = os_exe_async(command_list=command_list)
    for _x in res:
        _x.__str__(logger_info=logger.info,
                   logger_error=logger.error, flag="CMD")


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

    ZippFile(outpathzip, call_log_info=logger.info, call_log_error=logger.error).writePath(
        indir,
        # Исключим папку в которой находятся архивы
        execute_path={"zip"}
    )


def getlog_():
    """
    Получить пути к лог файлам
    """
    print(
        f"info: {path.abspath(PATH_INFO_LOG)}\nerror: {path.abspath(PATH_ERROR_LOG)}\n")
