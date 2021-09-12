# REST API для сервиса YaMDb- база отзывов о фильмах, книгах и музыке.
С использованием Continuous Integration и Continuous Deployment. При пуше в ветку main автоматически отрабатывают сценарии:

* Автоматический запуск тестов,
* Обновление образов на Docker Hub,
* Автоматический деплой на боевой сервер,
* Отправка сообщения в телеграмм-бот в случае успеха.
## Начало работы
Клонируйте репозиторий на локальную машину.
```python
git clone <адрес репозитория>
```
Для работы с проектом локально - установите вирутальное окружение и восстановите зависимости.
```python
python -m venv venv
pip install -r requirements.txt
```
### Подготовка удаленного сервера для развертывания приложения
Для работы с проектом на удаленном сервере должен быть установлен Docker и docker-compose. Эта команда скачает скрипт для установки докера:
```python
curl -fsSL https://get.docker.com -o get-docker.sh
```
Эта команда запустит его:
```python
sh get-docker.sh
```
Установка docker-compose:
```
apt install docker-compose
```
Создайте папку проекта на удаленном сервере и скопируйте туда файлы docker-compose.yaml, Dockerfile, host.conf:
```
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/yamdb_final/
```
### Подготовка репозитория на GitHub
Для использования Continuous Integration и Continuous Deployment необходимо в репозитории на GitHub прописать Secrets - переменные доступа к вашим сервисам. Переменые прописаны в workflows/yamdb_workflow.yaml
```python
DOCKER_PASSWORD, DOCKER_USERNAME - для загрузки и скачивания образа с DockerHub
USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу
DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT - для подключения БД
TELEGRAM_TO, TELEGRAM_TOKEN - для отправки сообщений в Telegram
```
### Развертывание приложения
При пуше в ветку main приложение пройдет тесты, обновит образ на DockerHub и сделает деплой на сервер. Дальше необходимо подключиться к серверу.
```python
ssh <USER>@<HOST>
```
Перейдите в запущенный контейнер приложения командой:
```pytho
docker container exec -it <CONTAINER ID> bash
```
Внутри контейнера необходимо выполнить миграции и собрать статику приложения:
```python
python manage.py collectstatic --no-input
python manage.py migrate
```
Для использования панели администратора по адресу http://0.0.0.0/admin/ необходимо создать суперпользователя.
```python
python manage.py createsuperuser.
```
К проекту по адресу http://0.0.0.0/redoc/ подключена документация API. В ней описаны шаблоны запросов к API и ответы. Для каждого запроса указаны уровни прав доступа - пользовательские роли, которым разрешён запрос.

## Технологии используемые в проекте
* Python, 
* Django, 
* Django REST Framework, 
* PostgreSQL, 
* Nginx, 
* Docker, 
* GitHub Actions
* DevOps

## Автор
ILDAR SALIAKHOV - автор, студент курса Python-разработчик в Яндекс.Практикум. Это учебный проект. Если есть вопросы или пожелания по проекту пишите на почту - saliakhovif@yandex.ru

## Бэйдж
![YaMDb-app workflow](https://github.com/ildarick93/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
