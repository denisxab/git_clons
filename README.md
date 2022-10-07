## Что это ?

Это программа поможет вам с локальным хранением репозиториев и `Gists`, которые хранятся на `Github`.

- **Зачем это** = Например, есть у вас более 20 репозиториев, и вы очень дорожите ими, что храните их на внешних носителях, и на различных устройствах. Скачивать и обновлять каждый репозиторий в ручную долго, поэтому создана это программа, для автоматизации этой задачи.

- **Почему не на Bash ?** = потому что на `Python` легче реализовать асинхронную работу с сетью. Благодаря асинхронности мои 50 репозиториев клонируются за 2 минуту, а `pull` выполняется за 30 секунд.

## Установка

1. Скачать `gitclones` из репозитория
2. Добавить `alias` в оболочку

   ```bash
   alias -g gitclones="ПУТЬ/git_clons/venv/bin/python3.10 ПУТЬ/git_clons/git_clons/main.py"
   ```

3. Проверим что вы указали верный путь

   ```bash
   gitclones --help
   ```

## Как пользоваться

1. **Сформировать конфигурационный файл** для указанного профиля. В него попадут ссылки на все публичные репозитории и `Gist`, и общая информация о профиле. По умолчанию файл будет расположен по пути `./look.json`.

   ```bash
   gitclones getrep ИмяПользователяGitHub -t ghp_ТокенGithub
   ```

   - **Внимание**, приватные репозитории не будут получены, их нужно указывать вручную в этом же файле `look.json`. Они не будут удалятся при следующей команде `getrep`, при этом токен который указан в их `URL` будет обновлен на, то что вы передали в параметре `-t`(это полезная вещь, когда срок вашего токена истек, и вам нужно его обновить на новый).

     _Пример ручного добавления репозитория_

     ```js
     "all_repos": {
         ...,
         "ИмяПроекта": {
             "visibility": "private",
             "clone_url": "https://USERNAME:TOKEN@github.com/denisxab/ИмяПроекта.git",
             "default_branch": "ИмяВеткиПоУмолчанию"
         }
         ...,
     }
     ```

2. После того как вы создали конфигурационный файл через команду `getrep`, выполните эту команду для **клонирования** репозиториев, и скачивания `Gist`. В опцию `-o` укажите куда клонировать репозитории.

   ```bash
   gitclones clones -o ПутьКудаКлонировать
   ```

3. После того как вы клонировали репозитории, вы можете за одну команду выполнить **`git pull`** для всех репозиториев.

   ```bash
   gitclones cmd pull -i ПутьК_ПапкеС_Репозиториями
   ```

   Вместо `pull` можно указать любу другую команду
