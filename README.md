### Как запустить проект?
Перейти в нужный репозиторий командной строкой:
```
cd ***
```
Клонировать репозиторий:
```
git clone git@github.com:lilyoungogbebra/api_final_yatube.git
```
Создать и активировать виртульное окружение для Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Создать и активировать виртульное окружение для Mac или Linux:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
