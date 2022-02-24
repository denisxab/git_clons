from os import path, makedirs, listdir
from time import time

from mg_file.file.json_file import JsonFile
from mg_file.file.zip_file import ZippFile
from mg_file.logsmal.logsmal import logger, loglevel
from mg_file.pcos.base_pcos import os_exe_thread

from pars_git import ParseGit

PATH_INFO_LOG = "./log/info.log"
PATH_ERROR_LOG = "./log/error.log"

logger.info = loglevel(
    "[INFO]",
    PATH_INFO_LOG,
    console_out=False,
    max_size_file="1mb"
)
logger.error = loglevel(
    "[ERROR]",
    PATH_ERROR_LOG,
    console_out=False,
    max_size_file="1mb",
)


def get_rep(user_name: str, outfile: str, token: str):
    """
    Получить данные с сервера ``GitHub``

    python main.py getrep denisxab

    :param user_name:
    :param outfile:
    :param token:
    """

    #:
    data_in_file = JsonFile(outfile).readFile()
    res = ParseGit(user_name=user_name, token=token)
    if data_in_file:
        res['all_repos'].update(data_in_file['all_repos'])
    # Записать данные в файл
    JsonFile(outfile).writeFile(res, sort_keys=False)


def clones_(path_look: str, outdir: str):
    """
    Клонировать репозитории


    :param outdir: Куда клонировать репозитории
    :param path_look: Путь к файлу с настройками
    """

    command_list: list[str] = []
    res: dict = JsonFile(path_look).readFile()
    for _name_rep, _val_rep in res["all_repos"].items():
        command_list.append(f"git clone {_val_rep['clone_url']} {path.join(outdir, _name_rep)}")

    os_exe_thread("CLONE", command_list, call_log_info=logger.info, call_log_error=logger.error)


def cmd_(command: str, indir: str, ):
    """
    Выполнить команду в каждом репозитории


    :param command:
    :param indir:
    """

    command_list: list[str] = []
    for _path in listdir(indir):
        if path.isdir(path.join(indir, _path)):
            command_list.append(f"cd {path.join(indir, _path)} && git {command}")

    os_exe_thread(command, command_list, call_log_info=logger.info, call_log_error=logger.error)


def zip_(outpathzip: str, indir: str):
    """
    Архивировать репозитории

    :param outpathzip:
    :param indir:
    """

    if outpathzip is None:
        makedirs(f"{indir}/zip", exist_ok=True)
        outpathzip = f"{indir}/zip/git_zip{int(time())}.zip"

    ZippFile(outpathzip).writePath(
        indir,
        # Исключим папку в которой находятся архивы
        execute_path={"zip"}
    )
