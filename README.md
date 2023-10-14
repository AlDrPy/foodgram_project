# **Foodgram**
#### _Ваш продуктовый помощник_
___
### Описание
##### **Foodgram** помогает своим пользователям создавать неповторимые рецепты, которыми обязательно захочется поделиться. Просматривайте рецепты других пользователей, добавляйте их в избранное, подписывайтесь на авторов понравившихся блюд. В Вашем распоряжении тысячи ингредиентов для создания собственных рецептов, а также возможность выгрузить перечень всех продуктов для рецептов, добавленных в список покупок. Удобная фильтрация по тегам "завтрак", "обед" и "ужин" поможет сориентироваться при поиске блюд, а подсказки при вводе названий ингредиентов помогут выбрать именно те продукты, которые нужны для Вашего кулинарного шедевра.

### Технологии

- Python + Django Rest Framework (API)
- WSGI сервер Gunicorn
- JavaScript + React (фронтенд)
- СУБД PostgreSQL
- Web сервер Nginx
- Контейнеризация Docker Compose
- CI/CD GitHub Actions


### Инструкция по запуску

Для работы проекта необходимо ядро ОС Linux и установленный в нём Docker с утилитой docker-compose. Также потребуется логин на Docker Hub. 

Пользователям ОС Windows потребуется витуальная машина Linux, либо утилита WSL2 и Git Bash для работы с Docker в командной строке. Во втором случае, в начале всех команд с флагами -it (интеракивный режим) необходимо добавлять "winpty" без кавычек,  для корректного отображения вывода терминала.

#### Локальный запуск проекта в контейнерах

- Клонировать репозиторий с GitHub:

  ```git clone https://github.com/AlDrPy/foodgram-project-react```

- В директории ```infra/``` с файлом ***docker-compose.yml*** выполнить команду
```docker compose up```

- Проверить, успешно ли прошёл запуск контейнеров, поможет команда
```docker compose ps```
Контейнер фронтенда должен скопировать статику и остановиться с _exit code 0_, после чего в работе должны остаться три контейнера: база данных, веб-сервер Nginx и бэкенд.

- После успешного запуска контейнеров, необходимо открыть терминал bash внутри контейнера backend (в Windows команда предваряется ```winpty```):
```docker compose exec -it backend bash```

- Внутри контейнера нужно выполнить миграции...
 ```python manage.py migrate```
...и создать суперпользователя:
```python manage.py createsuperuser```

  Статику бэкенда можно загрузить командой
  ```python manage.py collectstatic```

- В адресной строке браузера проект будет доступен по адресам:
  ***Главная страница:*** ```http://127.0.0.1:8000/```
  ***Панель администратора:*** ```http://127.0.0.1:8000/admin/```


#### Запуск проекта на удалённом сервере с ОС Linux Ubuntu

На сервере должно быть свободное дисковое пространство не менее 20 Гб, и установлен Docker с утилитой docker-compose.

- Перед развёртыванием проекта рекомендуется очистить кеш и логи приложений, и удалить неиспользуемые образы docker:
```sudo apt-get clean```
```sudo npm cache clean --force```
```sudo journalctl --vacuum-time=1d```
```sudo docker image rm $(sudo docker image ls -f "dangling=true" -q)```
_(более глубокая очистка docker):_ ```sudo docker system prune -a --force```

- Копировать файл ***docker-compose.production.yml*** на сервер

- В директории с файлом ***docker-compose.production.yml*** выполнить команды:

    - ```sudo docker compose -f docker-compose.production.yml pull``` (получить образы с Docker Hub)
    - ```sudo docker compose -f docker-compose.production.yml up -d``` (запустить контейнеры в фоновом режиме)
    - ```sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate``` (выполнить миграции БД)
    - ```sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic``` (собрать статику бэкенда)
    - ```sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/```  (копировать статику бэкенда в директорию, связанную с volume, откуда веб-сервер Nginx раздаёт всю статику проекта).
    
- После выполнения перечисленных выше действий приложение будет доступно на порту 8000.

### Авторы
_AlDrPy  https://github.com/AlDrPy_

***
``` Данные суперюзера для ревью ```

логин: alex
почта: random@random.com
пароль: random123456

```Адрес удаленного сервера```

ip: 84.201.161.167