import pprint
import subprocess
from os import makedirs, path, listdir
import os
from pathlib import Path
import re
from logsmal import logger
from mg_file.file.json_file import JsonFile
from mg_file.pcos.base_pcos import os_exe_async, type_os_res
from httpx import ConnectTimeout

from pars_git import ParseGit, T_all_gists, T_all_gists_files, TypeRepos


PATH_INFO_LOG = "./log/info.log"
PATH_ERROR_LOG = "./log/error.log"

logger.info.fileout = PATH_INFO_LOG
logger.error.fileout = PATH_ERROR_LOG


def getconf_(user_name: str, outfile: str, token: str):
    """
    Получить данные с сервера ``GitHub``, по умолчанию данные сохранятся
    в файл ``./gitconf.json``

    :param user_name: Имя пользователя GitHub
    :param outfile: Куда поместить файл с результатом
    :param token: Токен пользователя GitHub *пока не используется в логики программы*

    """
    #: Получить данные из существующей конфигурации
    data_in_file = JsonFile(outfile).readFile()
    try:
        res = ParseGit(user_name=user_name, token=token)
        if data_in_file:
            # Переносим закрытые репозитории из текущего файла. И обновляем токен в
            # URL клонирования, на тот который мы передали.
            d = {}
            for k, v in data_in_file['all_repos'].items():
                # Только закрытые репозитории
                if v['visibility'] == TypeRepos.private.value:
                    # Обновляем токен, если он передан
                    if token:
                        v['clone_url'] = token.join(
                            re.search('(.+:).+(@.+)',
                                      v['clone_url']).group(1, 2)
                        )
                    d[k] = v
            res['all_repos'].update(d)
        # Записать данные в файл
        JsonFile(outfile).writeFile(res, sort_keys=False)
        print("END")
    except ConnectTimeout as e:
        logger.error(e, 'Привешен лимит ожидания')


def sync_(path_conf: Path, outdir: str):
    """
    Синхронизация с конфигурациями

    :param path_conf: Путь к файлу с настройками
    :param outdir: Куда клонировать репозитории


    Итоговая структура:


    """
    # Конфигурация
    conf: dict = JsonFile(path_conf).readFile()
    # Список команд для асинхронного выполнения.
    async_command_list: list[str] = []

    def sync_rep():
        # 0. Для синхронизации репозиториев
        path_dir_rep = outdir / 'rep'
        makedirs(path_dir_rep, exist_ok=True)
        all_repos: dict[str, T_all_gists] = conf["all_repos"]
        async_command_rep: list[str] = []
        # 1. Проверяем наличие репозитория
        dir_rep: set[str] = set(os.listdir(path_dir_rep))
        for _name_rep, _val_rep in all_repos.items():
            path_rep: Path = path_dir_rep / _name_rep
            # 1.1. Если нет репозитория то формируем команды для его скачивания
            if not _name_rep in dir_rep:
                async_command_rep.append(
                    f"git clone {_val_rep['clone_url']} {path_rep}")
            # 1.2. Если есть репозитория, то проверить его url.
            else:
                # получаем url для кодирования репозитория
                url_rep = subprocess.check_output(
                    f"cd {path_rep.resolve()} && git remote get-url origin", shell=True)
                # 1.2.1 Если url не совпадает(например из за семы токена), то обновляем url в репозитории.
                if url_rep != _val_rep['clone_url']:
                    subprocess.check_output(
                        f"cd {path_rep.resolve()} && git remote set-url origin {_val_rep['clone_url']}", shell=True)
                # 1.2.2 Формируем команды для `pull``
                async_command_rep.append(f"cd {path_rep.resolve()} && git pull")
        return async_command_rep
    async_command_list.extend(sync_rep())

    def sync_gists():
        # 0. Для синхронизации Gists
        async_command_gists: list[str] = []
        p_dir_gists = outdir / 'gits'
        makedirs(p_dir_gists, exist_ok=True)
        all_gists: dict[str, T_all_gists] = conf["all_gists"]
        for _name_gists, _val_gists in all_gists.items():
            _val_gists: T_all_gists
            # Папка с Gists в кортом хранятся сами файлы
            p_dir_filename_gists = p_dir_gists / _name_gists
            # 1. Работаем с файлами Gists
            for g_name, g_val in _val_gists["files"].items():
                g_val: T_all_gists_files
                # 1.1 Делаем корректное название для папки с Gists
                _name_gists_file = re.search('(.+)(?:\.|\Z)', g_name).group(1)
                # 1.2 Создаем папки с именем файла Gists, это нужно для того чтобы хранить несколько версий файла gists
                path_name_gists_file: Path = p_dir_filename_gists/_name_gists_file
                makedirs(path_name_gists_file, exist_ok=True)
                path_name_gists_file_version = path_name_gists_file / \
                    g_val["version"]
                # 1.3 Если нет локальной версии которая указана в конфигурации, или если есть локальная версия, но в ней нет файла.
                if not path_name_gists_file_version.exists() or (path_name_gists_file_version.exists() and not os.listdir(path_name_gists_file_version)):
                    makedirs(path_name_gists_file_version, exist_ok=True)
                    # То тогда формируем команды для скачивания файлов Gists
                    async_command_gists.append(
                        f'''curl -s {g_val['raw_url']} > "{(path_name_gists_file_version/g_name).resolve()}"'''
                    )
        return async_command_gists
    async_command_list.extend(sync_gists())

    # logger.info(pprint.pformat(async_command_list))
    # Выполняем команды асинхронно
    res: list[type_os_res] = os_exe_async(command_list=async_command_list)
    res.sort(key=lambda k: k.cod)
    for _x in res:
        _x.__str__(
            logger_info=logger.info,
            logger_error=logger.error, flag="CLONES"
        )


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


# def zip_(outpathzip: Optional[str], indir: str):
#     """
#     Архивировать репозитории

#     :param outpathzip: Куда сохранить архив. По умолчанию там же где
#         ``indir`` в папке `zip/git_zip{время}.zip`
#     :param indir: Путь к папке с репозиториями


#     :Пример запуска:

#     .. code-block:: text

#         python main.py zip -i /home/denis/prog/GIT/
#     """
#     if outpathzip is None:
#         makedirs(f"{indir}/zip", exist_ok=True)
#         outpathzip = f"{indir}/zip/git_zip{int(time())}.zip"

#     ZippFile(outpathzip, call_log_info=logger.info, call_log_error=logger.error).writePath(
#         indir,
#         # Исключим папку в которой находятся архивы
#         execute_path={"zip"}
#     )


def getlog_():
    """
    Получить пути к лог файлам
    """
    print(
        f"info: {path.abspath(PATH_INFO_LOG)}\nerror: {path.abspath(PATH_ERROR_LOG)}\n")
