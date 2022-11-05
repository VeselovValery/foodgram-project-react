# Продуктовый помощник Foodgram

Проект доступен по адресу: 51.250.101.247

Логин администратора: manik86@yandex.ru

Пароль администратора: pas_manik_86

## Описание проекта Foodgram
«Продуктовый помощник» - это web-приложение, где пользователь может сформировать список покупок, которые он должен будет приобрести в достаточном количестве для приготовления блюд из понравившихся своих рецептов или рецептов сторонних авторов. Пользователи могут публиковать свои рецепты, а также довавлять в избранное или список покупок свои или чужие рецепты. Из вкладки "Список покупок" можно сформировать список продуктов, которые необходимо будет приобрести.

## Запуск проекта с использованием технологии Docker Сompose
Установить Docker, Docker Compose на сервере ВМ Yandex.Cloud:
```bash
ssh username@public_ip  # Заходим на свой сервер
sudo apt install curl  # Устанавливаем утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh  # Скачиваем скрипт для установки докера
sh get-docker.sh   # Запускаем докер
sudo apt update  # Обновить список пакетов
# Установить необходимые пакеты для загрузки через https
sudo apt install \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  # Добавляем ключ GPC для подтверждения подлиночти
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"  # Добавляем репозиторий Docker в пакеты apt
sudo apt update  # Снова обновляем список пакетов
sudo apt install docker-ce docker-compose -y  # Устанавливаем Docker и Docker Compose
```
Установить систему контроля версий git:
```bash
sudo apt install git -y
```
Клонировать проект с использованием системы контроля версий git:
```bash
git clone you_ssh_link
```
Перейти к месту расположения файла для запуска Docker Compose:
```bash
cd foodgram-project-react/infra
```
Заполнить файл .env для секретной информации:
```python
DB_ENGINE='django.db.backends.postgresql'
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT='5432'
SECRET_KEY=
```
Запустить контейнеры для развертывания приложения:
```bash
sudo docker-compose up -d
```
Выполнить миграции:
```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```
Создать администратора приложения:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
Собрать статические файлы:
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Наполнить базу данных ингредиентами:
```bash
sudo docker-compose exec backend python manage.py load_ingredients
```
## Примеры запросов API проекта Foodgram
### 1. Пользователи
1.1. GET-запрос на http://you_public_ip/api/users/ возвращает список пользователей. Авторизация пользователя в данном запросе не требуется.

1.2. POST-запрос на http://you_public_ip/api/users/ в виде:
```bash
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
создает нового пользователя с указанными данными. Авторизация пользователя в данном запросе не требуется. Все поля обязательны для заполнения.

1.3. GET-запрос на http://you_public_ip/api/users/{id}/ возращает данные о пользователе id которого указан. При данном запросе необходима авторизация пользователя.

1.4. GET-запрос на http://you_public_ip/api/users/me/ возвращает данные о текущем пользователе, который производит данный запрос.

1.5. POST-запрос на http://you_public_ip/api/users/set_password/ в виде:
```bash
{
  "new_password": "string",
  "current_password": "string"
}
```
производит смену пароля авторизованного пользователя, отправившего данный запрос. Все поля обязательны для заполнения.

1.6. POST-запрос на http://you_public_ip/api/auth/token/login/ в виде:
```bash
{
  "password": "string",
  "email": "string"
}
```
производит авторизацую пользователя с выдачей токена для его дальнейшего использования в запросах авторизированных пользователей. Все поля обязательны для заполнения.

1.7. POST-запрос на http://you_public_ip/api/auth/token/logout/ удаляет токен текущего авторизованного пользователя.

### 2. Теги
2.1. GET-запрос на http://you_public_ip/api/tags/ возвращает список тегов сохранненных в базе данных. Авторизация пользователя в данном запросе не требуется.

2.2. GET-запрос на http://you_public_ip/api/tags/{id} возвращает информацию о теге, id которого передан в запросе. Авторизация пользователя в данном запросе не требуется.

### 3. Рецепты
3.1. GET-запрос на http://you_public_ip/api/recipes/ возвращает список рецептов сохраненных в базе данных. Авторизация пользователя в данном запросе не требуется.

3.2. POST-запрос на http://you_public_ip/api/recipes/ в виде:
```bash
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
создает рецепт от имени текущего авторизованного пользователя. Все поля обязательны для заполнения.

3.3. GET-запрос на http://you_public_ip/api/recipes/{id}/ возвращает информацию о рецепте, id которого был передан в запросе. Авторизация пользователя в данном запросе не требуется.

3.4. PATCH-запрос на http://you_public_ip/api/recipes/{id}/ в виде:
```bash
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
производит смену данных по рецепту, id которого был передан в запросе. Смена данных может осущетсвляться только авторизованным пользователем - автором данного рецепта.

3.5. DELETE-запрос на http://you_public_ip/api/recipes/{id}/ производит удаленние рецепта, id которого был передан в запросе. Удаление рецепта может осуществляться только авторизованным пользователем - автором данного рецепта.

### 4. Список покупок
4.1. GET-запрос на http://you_public_ip/api/recipes/download_shopping_cart/ отправляет текущему авторизованному пользователю список покупок в формате TXT. 

4.2. POST-запрос на http://you_public_ip/api/recipes/{id}/shopping_cart/ добавляет рецепт, id которого указан в запросе в продуктовую корзину текущего авторизованного пользователя.

4.3. DELETE-запрос на http://you_public_ip/api/recipes/{id}/shopping_cart/ производит удаление рецепта, id которого указан в запросе из продуктовой корзины текущего авторизованного пользователя.

### 5. Избранное
5.1. POST-запрос на http://you_public_ip/api/recipes/{id}/favorite/ добавляет рецепт, id которого указан в запросе в избранное текущего авторизованного пользователя.

5.2. DELETE-запрос на http://you_public_ip/api/recipes/{id}/favorite/ удаляет рецепт, id которого указан в запросе из избранного текущего авторизированного пользователя.

### 6. Подписки
6.1. GET-запрос на http://you_public_ip/api/users/subscriptions/ возвращает информацию об авторах, на которых подписан текущий авторизирован пользователь.

6.2. POST-запрос на http://you_public_ip/api/users/{id}/subscribe/ производит подписку текущего авторизованного пользователя на автора, id которого указан в запросе.

6.3. DELETE-запрос на http://you_public_ip/api/users/{id}/subscribe/ производит отписку текущего авторизованного пользователя от автора, id которого указан в запросе.

### 7. Ингредиенты
7.1. GET-запрос на http://you_public_ip/api/ingredients/ возвращает список ингредиентов сохранненных в базе данных. Авторизация пользователя в данном запросе не требуется.

7.2. GET-запрос на http://you_public_ip/api/ingredients/{id} возвращает информацию об ингредиенте, id которого передан в запросе. Авторизация пользователя в данном запросе не требуется.

Более подробную информацию о запросах и ответах на все end-point можно посмотреть в документации API:  http://you_public_ip/api/docs/

## Технологии использованные в проекте Foodgram
1. Django
2. Django REST-Framework
3. Djoser
4. Docker
5. Docker Compose

## Об авторе
Автор: [Веселов Валерий](https://github.com/VeselovValery)
