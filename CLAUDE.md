# Demoblaze API Test Framework

Портфолио-проект. Переношу структуру своего курсового `api-fixtures-homework`
(API-only, без UI) на публичный демо-магазин demoblaze.com.

## Правила работы

- Отвечать по-русски, кратко.
- Объяснять так, чтобы я писал код руками, а не копипастил. Давай куски по
  одной функции с пояснением, а не готовые файлы целиком.
- Не выдумывать эндпоинты и тела запросов. Всё, что не подтверждено прогоном,
  помечено ниже как НЕ ПОДТВЕРЖДЕНО — сначала разведка, потом код.
- Windows, PowerShell, PyCharm, Python 3.11.

## Целевой стенд

Base URL API: `https://api.demoblaze.com`
Фронт: `https://www.demoblaze.com`

Стенд публичный и общий для всех — данные не изолированы. Отсюда следуют
жёсткие требования:
- каждый тест сам создаёт себе юзера (Faker), никаких хардкод-кредов;
- всё созданное чистится в teardown;
- никаких ассертов на «в корзине ровно N товаров» без привязки к своему токену.

## Контракт API

### Подтверждено реальным запросом

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

- 9 товаров на страницу, пагинация через `LastEvaluatedKey` (ключ DynamoDB).
- Категории: `phone`, `notebook`, `monitor`.
- Query-параметр `?id=9` игнорируется — пагинация передаётся иначе.

### НЕ ПОДТВЕРЖДЕНО — разведать через tools/probe_demoblaze.py

Ни методы, ни тела этих запросов не проверены. Предположительно POST:
`/bycat`, `/view`, `/signup`, `/login`, `/addtocart`, `/viewcart`,
`/deleteitem`, `/deletecart`.

Отдельно проверить: пароль кодируется base64 на клиенте — кодирует ли
бэкенд сам, или ждёт готовый base64. Скрипт регистрирует двух юзеров
(с кодировкой и без) специально для этого.

## Найденные баги (в README как bug report)

1. `title` товара id=9 содержит хвостовой перевод строки: `"Sony vaio i7\n"`.
2. Товары id=4, 8, 9 переиспользуют чужие картинки (`galaxy_s6.jpg`,
   `sony_vaio_5.jpg`).
3. Пароль кодируется base64 (обратимая кодировка), а не хешируется.

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
│   │   ├── product.py         # Product, EntriesResponse — можно писать сейчас
│   │   ├── auth.py            # после probe
│   │   └── cart.py            # после probe
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
│   ├── data_generator.py      # Faker: юзер, пароль
│   ├── retry.py               # get_with_retry из курсового
│   ├── encoders.py            # encode_password (base64)
│   ├── assertions.py          # assert_status_code с телом ответа в ошибке
│   └── cleanup.py             # чистка корзины после теста
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
| `guest` | `guest` | без токена |
| `test_item` | `test_product` | берётся из `/entries`, не создаётся |

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

- логин: JSON + base64, а не form-data OAuth2;
- нет ролей и нет CRUD пользователей — вместо `test_users.py` и `test_roles.py`
  пишется `test_cart.py`;
- нет доступа к БД — DB-ассерты заменяются на проверки через API;
- CI на GitHub Actions вместо GitLab CI.
