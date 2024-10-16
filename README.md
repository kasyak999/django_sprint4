## Проекту django_sprint4

[Ссылка на описание](#описание)

### Установка

1. создать виртуальное окружение
    ```bash 
    python -m venv venv
    ```
    ```bash 
    source venv/bin/activate
    ```
2. Установить зависимости
    ``` bash
    pip install -r requirements.txt
    ```
3. Установить миграции
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```
4.  Запустить
    ```bash
    python manage.py runserver
    ```

### Необходимые условия

- Версия Python: 3.9
- ОС: Windows, Linux, MacOS
- Менеджер пакетов: pip
- БД: SQLite

## Описание
Вот перечень задач, которые выполнены:

- **Кастомные страницы для ошибок.**

    Подключите к проекту и настройте кастомные страницы для ошибок 403 CSRF, 404 и 500. Шаблоны для этих страниц находятся в директории templates/pages/.

- **Работа с пользователями.**

    Подключите к проекту пользователей:
    1. Подключите к проекту пути для работы с пользователями из ```django.contrib.auth.urls```.
    2. Переопределите шаблоны для каждой подключённой страницы.
    3. Создайте страницу **auth/registration/** с формой для регистрации пользователей.
    4. Создайте страницу пользователя **profile/<username\>/**. На ней должны отображаться:
        - информация о пользователе (доступна всем посетителям),
        - публикации пользователя (доступны всем посетителям),
        - ссылка на страницу редактирования профиля для изменения имени, фамилии, логина и адреса электронной почты (доступна только залогиненному пользователю — хозяину аккаунта),
        - ссылка на страницу изменения пароля (доступна только залогиненному пользователю — хозяину аккаунта).

    Переопределять встроенную модель пользователя не требуется.

- **Пагинация.**

    Подключите к проекту пагинацию и настройте вывод не более 10 публикаций

    - на главную страницу,
    - на страницу пользователя,
    - на страницу категории.

- **Изображения к постам.**

    Добавьте возможность прикреплять изображение к публикациям проекта. Если изображение добавлено, то оно должно отображаться в публикациях на

    - главной странице,
    - странице пользователя,
    - странице категории,
    - отдельной странице публикации.

- **Добавление новых публикаций.**

    У зарегистрированных пользователей должна быть возможность самостоятельно публиковать посты. Создайте страницу для публикации новых записей **posts/create/**:

    1. Страница добавления публикации должна быть доступна только авторизованным пользователям.
    2. После валидации формы и добавления новой публикации пользователь должен быть перенаправлен на свою страницу **profile/<username\>/**.
    3. Новые категории и местоположения может создавать только администратор сайта через панель администратора.
    4. Указав дату публикации «в будущем», можно создавать отложенные посты. Они должны стать доступны всем посетителям с момента, указанного в поле «Дата». Отложенные публикации должны быть доступны автору сразу же после отправки; автор должен видеть на своей странице все свои публикации, включая отложенные и снятые с публикации администратором.

- **Редактирование публикаций.**

    Добавьте страницу редактирования публикации с адресом **posts/<post_id>/edit/**.

    - Права на редактирование должны быть только у автора публикации. Остальные пользователи должны перенаправляться на страницу просмотра поста.
    - Для страницы редактирования поста должен применяться тот же HTML-шаблон, что и для страницы создания нового поста: blog/create.html.
    - После окончания редактирования пользователь должен переадресовываться на страницу отредактированной публикации.

- **Комментарии к публикациям.**

    Создайте систему комментирования записей. На странице поста под текстом записи должна выводиться форма для отправки комментария, а ниже — список комментариев.

    - Комментарии должны быть отсортированы по времени их публикации, «от старых к новым».
    - Комментировать публикации могут только авторизованные пользователи.
    - Авторы комментариев должны иметь возможность отредактировать собственные комментарии.
    - Для каждой публикации на
        - главной странице,
        - странице пользователя,
        - странице категории

        нужно выводить количество комментариев.
    - Адрес для добавления комментария **posts/<post_id>/comment/**
    - Адрес для редактирования комментария **posts/<post_id>/edit_comment/<comment_id>/**

- **Удаление публикаций и комментариев.**

    Авторизованные пользователи должны иметь возможность удалять собственные публикации и комментарии. Перед удалением материала должна открываться подтверждающая страница, содержащая публикацию или комментарий. Для подтверждающей страницы не надо создавать отдельные шаблоны; для этого необходимо переиспользовать существующие шаблоны, необходимая логика в них уже присутствует.
    - Адрес для удаления публикации **posts/<post_id>/delete/**
    - Адрес для удаления комментария **posts/<post_id>/delete_comment/<comment_id>/**

- **Новые статичные страницы.**

    Обновите механизм создания и изменения статичных страниц в проекте, используя CBV. Адреса уже существующих статичных страниц не должны измениться.

- **Отправка электронной почты.**

    Подключать к проекту реальный почтовый сервер сейчас нет необходимости, поэтому подключите файловый бэкенд: все «отправленные» письма должны аккумулироваться в специальной директории проекта sent_emails/. Из репозитория проекта эту директорию стоит исключить.