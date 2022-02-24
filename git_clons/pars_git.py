import asyncio
from enum import Enum
from pprint import pformat
from string import Template
from time import process_time
from typing import Union, Final, TypedDict, Optional

from httpx import get, AsyncClient, Response
from logsmal import logger


class ApiGutHub(Enum):
    """
    Список URL API GitHub

    :Пример использования:

    .. code-block:: python

        ApiGutHub.all_rep.value.substitute(user_name='denisxab')
        # https://api.github.com/users/denisxab/repos
    """
    #: Получить список репозиториев у пользователя
    all_rep: Template = Template("https://api.github.com/users/$user_name/repos")
    #: Получить информацию о пользователи
    info_user: Template = Template("https://api.github.com/users/$user_name")


class Tall_repos(TypedDict):
    """
    Структура словаря для хранения проекта
    """
    #: Доступность проекта  public/private
    visibility: str
    #: Url для клонирования проекта
    clone_url: str
    #: Дата обновления проекта
    updated_at: str
    #: Основная ветка проект
    default_branch: str


class TGitUser(TypedDict):
    """
    Структура словаря для хранения профиль пользователя
    """
    #: Имя профиля
    user_name: str
    #: Токен пользователя
    token: str
    #: Данные о пользователе
    meta_user: dict[str, str]
    #: Все репозиторию пользователя
    all_repos: dict[str, Tall_repos]


class ParseGit:
    """
    Класс для парсинга профиля
    """

    #: Сколько можно получить репозиториев за одно обращение к серверу
    LEN_MAX_PROJ_ONE_PAGE: Final[int] = 90

    def __new__(cls, user_name: str, token: Optional[str] = None):
        """
        :param token: Токен пользователя
        :param user_name: Имя пользователя
        """
        start = process_time()
        info = cls.getInfo(user_name, token)
        GitUser: TGitUser = TGitUser(
            user_name=user_name,
            token=token,
            meta_user=info,
            all_repos=asyncio.run(cls.getRepository(user_name, info["count_public_repos"], token))
        )
        logger.info(process_time() - start, flag="TIME")
        logger.info(pformat(GitUser), flag="GIT_USER")
        return GitUser

    @classmethod
    def getInfo(cls, user_name: str, token: Optional[str]) -> dict[str, Union[str, int]]:
        """
        Получить информацию о пользователе

        :param token: Токен пользователя
        :param user_name: Имя пользователя
        """
        res: Response = get(
            url=ApiGutHub.info_user.value.substitute(user_name=user_name),
            headers=cls._getHeaders(token)
        )
        res.raise_for_status()
        rj = res.json()
        return {
            "login": rj["login"],
            "id": rj["id"],
            'gists_url': rj['gists_url'],
            'repos_url': rj['repos_url'],
            'count_public_repos': rj['public_repos'],
        }

    @classmethod
    async def getRepository(cls, user_name: str, count_public_repos: int, token: Optional[str]) \
            -> dict[str, dict[Union[str, int]]]:
        """
        Получить список всех репозиториев

        :param token: Токен пользователя
        :param user_name: Имя пользователя
        :param count_public_repos: Количество репозиториев
        :return: Список всех репозиториев пользователя
        """

        #: Переменная для ответа
        res: dict[str, dict[Union[str, int]]] = {}

        async def self_(_page):
            async with AsyncClient() as client:
                _res: Response = await client.get(
                    url=ApiGutHub.all_rep.value.substitute(user_name=user_name),
                    headers=cls._getHeaders(token),
                    params={
                        "per_page": cls.LEN_MAX_PROJ_ONE_PAGE,
                        "page": _page
                    }
                )
            logger.info(_res.url, flag="URL")
            for x in _res.json():
                res[x['name']] = Tall_repos(
                    visibility=x['visibility'],
                    clone_url=x["clone_url"],
                    updated_at=x["updated_at"],
                    default_branch=x["default_branch"],
                )

        tasks = [self_(page) for page in range(1, count_public_repos // cls.LEN_MAX_PROJ_ONE_PAGE
                                               # для округления в большую строну
                                               + 1
                                               # для того чтобы даже одна страница загрузилась
                                               + 1)]
        await asyncio.gather(*tasks)
        return res

    @staticmethod
    def _getHeaders(token: Optional[str]):
        #: Заголовки для запроса в формате json
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        # Аутентификация по токину
        if token:
            headers["Authorization"] = "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"
