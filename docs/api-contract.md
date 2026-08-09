# Контракт API demoblaze.com

Публичной документации у стенда нет — ни OpenAPI, ни описания эндпоинтов.
Всё, что ниже, снято разведочным прогоном `tools/probe_demoblaze.py`: скрипт
бьёт по эндпоинтам-кандидатам, определяет HTTP-метод по ответу сервера и
печатает реальные тела запроса и ответа. Догадок и заимствований из
фронтенда здесь нет.

- **Base URL:** `https://api.demoblaze.com`
- **Фронт:** `https://www.demoblaze.com`
- **Проверено:** 9 августа 2026
- **Перепроверить:** `python tools/probe_demoblaze.py`

## Общие правила стенда

- **Все ответы приходят со статусом 200**, включая ошибки. Проверять надо
  тело, а не код.
- Ошибка лежит в теле в поле `errorMessage`:
  `{"errorMessage": "Bad parameter, token malformed."}`.
- `/entries` — единственный GET. Все остальные эндпоинты — POST с JSON.
- `/login` и `/deleteitem` при успехе отдают **текст, а не JSON**. При
  ошибке эти же эндпоинты отдают JSON с `errorMessage`. Поэтому
  `CustomRequester._parse` откатывается на `response.text`, если разбор
  JSON не удался.
- **Пароль передаётся открытым текстом**, base64 бэкендом не требуется:
  `/signup` сохраняет строку как есть, `/login` сравнивает её же. Base64 —
  чисто клиентская обёртка фронта. Важно лишь, чтобы регистрация и вход
  шли в одном формате.
- **Идентификатор позиции корзины генерирует клиент** — сервер принимает
  любой `id`, который прислали в `/addtocart`, и по нему же удаляет.

## Сводка эндпоинтов

| Метод | Путь | Назначение | Формат успешного ответа |
|---|---|---|---|
| GET | `/entries` | список товаров | JSON |
| POST | `/bycat` | товары по категории | JSON |
| POST | `/view` | один товар по id | JSON |
| POST | `/signup` | регистрация | JSON (пустая строка) |
| POST | `/login` | вход, выдаёт токен | **текст** |
| POST | `/addtocart` | добавить позицию в корзину | пустое тело |
| POST | `/viewcart` | содержимое корзины | JSON |
| POST | `/deleteitem` | удалить позицию корзины | **текст** |

## Каталог

| Запрос | Тело запроса | Успех | Ошибка |
|---|---|---|---|
| `GET /entries` | — | `{"Items": [...], "LastEvaluatedKey": {...}}` | не наблюдалась |
| `POST /bycat` | `{"cat": "phone"}` | `{"Items": [...]}` | не наблюдалась |
| `POST /view` | `{"id": "1"}` | объект товара без обёртки `Items` | не наблюдалась |

```
GET /entries  ->  200
{
  "Items": [
    {
      "id": 1,
      "cat": "phone",
      "title": "Samsung galaxy s6",
      "price": 360.0,
      "img": "imgs/galaxy_s6.jpg",
      "desc": "The Samsung Galaxy S6 is powered by..."
    }
  ],
  "LastEvaluatedKey": {"id": "9"}
}
```

- 9 товаров на страницу (id 1..9), пагинация через `LastEvaluatedKey`
  (ключ DynamoDB). Query-параметр `?id=9` игнорируется.
- Категории: `phone`, `notebook`, `monitor`.

```
POST /bycat   {"cat": "phone"}  ->  200  {"Items": [ ...та же форма... ]}
POST /view    {"id": "1"}       ->  200  {объект товара, без обёртки Items}
```

## Авторизация

| Запрос | Тело запроса | Успех | Ошибка |
|---|---|---|---|
| `POST /signup` | `{"username": "...", "password": "..."}` | `""` (пустая JSON-строка) | `{"errorMessage": "This user already exist."}` |
| `POST /login` | `{"username": "...", "password": "..."}` | `Auth_token: <base64>` (текст) | `{"errorMessage": "Wrong password."}` / `{"errorMessage": "User does not exist."}` |

```
POST /signup  {"username": "...", "password": "..."}
  успех:  200  ""                                        (пустая JSON-строка)
  ошибка: 200  {"errorMessage": "This user already exist."}

POST /login   {"username": "...", "password": "..."}
  успех:  200  Auth_token: cHJvYmVfN2UxMTc4Njgy...       (текст, не JSON)
  ошибка: 200  {"errorMessage": "Wrong password."}
               {"errorMessage": "User does not exist."}
```

Токен — это base64 от `<username><timestamp>`, без подписи. Декодируется
обратно чем угодно, целостность сервером не проверяется.

## Корзина

| Запрос | Тело запроса | Успех | Ошибка |
|---|---|---|---|
| `POST /addtocart` | `{"id": "<uuid>", "cookie": "<токен>", "prod_id": 1, "flag": true}` | пустое тело | не наблюдалась |
| `POST /viewcart` | `{"cookie": "<токен>", "flag": true}` | `{"Items": [...]}` | `{"errorMessage": "Bad parameter, token malformed."}` |
| `POST /deleteitem` | `{"id": "<uuid>"}` | `Item deleted.` (текст) | `{"errorMessage": "Not found."}` |

```
POST /addtocart  {"id": "<uuid клиента>", "cookie": "<токен>",
                  "prod_id": 1, "flag": true}
  ->  200  ""

POST /viewcart   {"cookie": "<токен>", "flag": true}
  успех:  200  {"Items": [{"id": "<uuid>", "cookie": "<username>",
                           "prod_id": 1}]}
  ошибка: 200  {"errorMessage": "Bad parameter, token malformed."}

POST /deleteitem {"id": "<uuid>"}
  успех:  200  Item deleted.                             (текст, не JSON)
  ошибка: 200  {"errorMessage": "Not found."}
```

Обратить внимание: в ответе `/viewcart` поле `cookie` содержит **имя
пользователя**, а не присланный токен. `/deleteitem` токен не принимает
вовсе — только `id` позиции.

## Что из этого следует для тестов

Дефекты стенда, обнаруженные при снятии контракта, перечислены в
[README](../README.md#найденные-дефекты).
