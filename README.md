# Yacut-укротитель ссылок

[Описание](#описание) /

[Запуск](#Запуск) /

## Описание

[Yacut](https://github.com/slavspart/yacut) сервис для создания промежуточных URL адресов, связанных с другими URL.
После создания промежуточного адреса, пользователь может использовать его для обращения к конечному URL.
Сервис предусматривает:
- пользовательский интерфейс (html-страница с формой);
- API для создания и получения промежуточных адресов.
Сервис создан на базе фрэймворка Flask.

## Запуск

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
```
flask run
```