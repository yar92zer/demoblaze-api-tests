# Demoblaze API Test Framework

Портфолио-проект. Переношу структуру своего курсового `api-fixtures-homework`
(API-only, без UI) на публичный демо-магазин demoblaze.com.

## Правила работы

- Отвечать по-русски, кратко.
- Объяснять так, чтобы я писал код руками, а не копипастил. Давай куски по
  одной функции с пояснением, а не готовые файлы целиком.
- Не выдумывать эндпоинты и тела запросов: сначала разведка через
  `tools/probe_demoblaze.py`, потом код. Раздел «Контракт API» ниже целиком
  снят прогоном — всё, что в него добавляется, добавляется так же.
- Windows, PowerShell, PyCharm, Python 3.11.

## Целевой стенд

Base URL API: `https://api.demoblaze.com`
Фронт: `https://www.demoblaze.com`

Стенд публичный и общий для всех — данные не изолированы. Отсюда следуют
жёсткие требования:
- каждый тест сам создаёт себе юзера (`uuid4`, префикс `qa_`), никаких
  хардкод-кредов;
- всё созданное чистится в teardown;
- никаких ассертов на «в корзине ровно N товаров» без привязки к своему токену.

## Контракт API

Весь раздел подтверждён прогоном `tools/probe_demoblaze.py`. Догадок нет.

### Общие правила стенда

- **Все ответы приходят со статусом 200**, включая ошибки. Проверять надо
  тело, а не код.
- Ошибка лежит в теле в поле `errorMessage`:
  `{"errorMessage": "Bad parameter, token malformed."}`.
- `/entries` — единственный GET. Все остальные эндпоинты — POST с JSON.
- `/login` и `/deleteitem` при успехе отдают **текст, а не JSON**. Поэтому
  `CustomRequester._parse` откатывается на `response.text`, если разбор
  JSON не удался. При ошибке эти же эндпоинты отдают JSON с `errorMessage`.
- **Пароль передаётся открытым текстом**, base64 бэкендом не требуется:
  `/signup` сохраняет строку как есть, `/login` сравнивает её же. Base64 —
  чисто клиентская обёртка фронта. Важно лишь, чтобы регистрация и вход
  шли в одном формате.
- **Идентификатор позиции корзины генерирует клиент** — сервер принимает
  любой `id`, который прислали в `/addtocart`, и по нему же удаляет.

### Каталог

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

### Авторизация

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

### Корзина

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

## Найденные баги (в README как bug report)

| № | Дефект | Severity |
|---|---|---|
| 1 | Токен авторизации не имеет подписи и обратимо декодируется — его содержимое восстанавливается из самого токена. Проверка целостности на стороне сервера отсутствует. | Critical |
| 2 | Ошибки возвращаются с кодом 200. Некорректный токен даёт `200 OK` с текстом ошибки в теле вместо 401/400. | Major |
| 3 | Пароль передаётся и сравнивается без хеширования. Кодирование на клиенте обратимо и не является защитой. | Major |
| 4 | `/deleteitem` не требует токена — принимает только идентификатор позиции корзины. Признаки IDOR. | Major |
| 5 | `/signup` при успехе возвращает пустое тело (`""`) — подтверждения операции в ответе нет. | Minor |
| 6 | Мусор в данных каталога: у товара id=9 в поле `title` хвостовой перевод строки (`"Sony vaio i7\n"`); картинки дублируются — id=4 ссылается на изображение товара id=1 (`galaxy_s6.jpg`), id=9 — на изображение товара id=8 (`sony_vaio_5.jpg`). | Trivial |

Дефекты 1 и 2 зафиксированы автотестами (`test_token_contains_username`,
`test_malformed_token_returns_error`) — тесты проверяют фактическое
поведение и упадут, если оно изменится.

## Структура

```
demoblaze-api-framework/
├── .github/workflows/ci.yml
├── CLAUDE.md
├── README.md
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── settings.py            # base_url, таймауты, ретраи из .env
│   └── endpoints.py           # Enum путей, заполнять по мере разведки
│
├── api/
│   ├── __init__.py
│   ├── custom_requester.py    # из курсового, слой транспорта
│   ├── models/
│   │   ├── product.py         # Product, EntriesResponse
│   │   └── cart.py            # CartItem, CartResponse
│   └── services/
│       ├── base_service.py
│       ├── catalog_service.py # get_entries, get_by_cat, get_view
│       ├── auth_service.py    # signup, login
│       └── cart_service.py    # add_to_cart, view_cart, delete_item
│
├── tests/
│   ├── conftest.py            # фикстуры (см. ниже)
│   └── api/
│       ├── test_catalog.py
│       ├── test_auth.py
│       └── test_cart.py
│
├── utils/
│   ├── data_generator.py      # uuid4: уникальный юзер, пароль
│   ├── retry.py               # with_retry из курсового
│   ├── encoders.py            # encode_password / decode_token (base64)
│   └── assertions.py          # assert_no_error, assert_status_code
│
└── tools/
    └── probe_demoblaze.py     # разведка контракта, запустить первым
```

## Фикстуры (адаптация курсовых шести)

| Курсовая | Здесь | Комментарий |
|---|---|---|
| `base_url` | `base_url` | без изменений |
| `db_connection` | **убрана** | БД чужая, доступа нет |
| `admin_user` | **убрана** | ролей у Demoblaze нет |
| `regular_user` | `authenticated_user` | signup + login, свежий на каждый тест |
| `test_item` | **убрана** | товары в каталоге статичны, создавать нечего |

Плюс сервисные фикстуры: `requester`, `catalog`, `auth`, `cart` (session)
и `cart_with_product` — добавляет товар и чистит его в teardown.

Источник правды для ассертов по данным — ответ `/viewcart`, а не БД.

## Маркеры

```ini
[pytest]
markers =
    smoke: критичный минимум, на каждый коммит
    regression: полный прогон
    negative: невалидные данные, чужие и битые токены
    auth: signup / login
    cart: корзина
```

## Порядок работ

1. Прогнать `tools/probe_demoblaze.py`, зафиксировать реальный контракт сюда.
2. Каркас: `settings.py`, `custom_requester.py`, `.env.example`, `pytest.ini`.
3. Первый зелёный тест на `/entries` (контракт уже известен).
4. Модели → сервисы → тесты, по одному домену: каталог, авторизация, корзина.
5. Хелперы и маркеры.
6. `.github/workflows/ci.yml`: джобы smoke / regression / parallel, Allure.
7. README с описанием архитектуры и bug report, push на GitHub.

## Чем отличается от курсового

- логин: JSON с паролем открытым текстом, а не form-data OAuth2;
- нет ролей и нет CRUD пользователей — вместо `test_users.py` и `test_roles.py`
  пишется `test_cart.py`;
- нет доступа к БД — DB-ассерты заменяются на проверки через API;
- CI на GitHub Actions вместо GitLab CI.
