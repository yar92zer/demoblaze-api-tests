[![Tests](https://github.com/yar92zer/demoblaze-test-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/yar92zer/demoblaze-test-framework/actions/workflows/ci.yml)

# Demoblaze Test Framework

Тестовый фреймворк для публичного демо-магазина demoblaze.com: API-клиент
(`https://api.demoblaze.com`), UI на Playwright (`https://www.demoblaze.com`)
и сквозные тесты, проверяющие, что оба слоя видят одни и те же данные.

Тесты идут против живого публичного стенда — нужен интернет, и красный прогон
может означать недоступность чужого сервиса.

[Allure-отчёт последнего прогона](https://yar92zer.github.io/demoblaze-test-framework) ·
[Контракт API](api-contract.md)

## Стек

Python 3.11, pytest, requests, Pydantic, Playwright, Allure, pytest-xdist, GitHub Actions

## Что покрыто

39 тестов:

| Слой | Тестов | Домены |
|---|---|---|
| `tests/api/` | 14 | каталог, авторизация, корзина, известные дефекты |
| `tests/ui/` | 22 | авторизация, каталог, корзина, заказ, контакты, известные дефекты |
| `tests/cross/` | 3 | сквозные API + UI |

Плюс 13 задокументированных дефектов стенда, три из них зафиксированы
`xfail(strict=True)` — почини стенд, и прогон покраснеет.

## Структура

```
demoblaze-test-framework/
├── .github/workflows/
│   ├── ci.yml                 lint + api + ui + nightly regression
│   └── pages.yml              сборка и публикация Allure на GitHub Pages
├── client/                    API-клиент
│   ├── custom_requester.py    транспорт: сессия, таймауты, разбор тела, Allure
│   ├── endpoints.py           пути эндпоинтов одним Enum
│   ├── services/              base, auth, cart, catalog
│   └── models/                Pydantic-валидация: product, cart
├── pages/                     Page Object'ы
│   ├── base_page.py           обёртки над Playwright
│   ├── home_page.py           витрина: категории, пагинация, карточки
│   ├── product_page.py
│   ├── cart_page.py
│   ├── header.py
│   ├── login_modal.py
│   ├── signup_modal.py
│   ├── order_modal.py
│   └── contact_modal.py
├── utils/
│   ├── data_generator.py      уникальный логин на каждый тест
│   ├── assertions.py          assert_no_error, assert_status_code
│   ├── encoders.py            base64: encode_password, decode_token
│   └── retry.py               with_retry поверх tenacity
├── tests/
│   ├── api/                   test_catalog, test_auth, test_cart, test_known_defects
│   ├── ui/                    + test_order, test_contacts
│   └── cross/                 test_api_ui
├── conftest.py                фикстуры обоих слоёв, скриншот при падении
├── settings.py                base_url, front_url, таймаут, ретраи из .env
├── probe_demoblaze.py         разведка контракта: чем снят api-contract.md
├── api-contract.md            подтверждённый контракт стенда
├── pytest.ini
├── ruff.toml
├── requirements.txt
└── .env.example
```

API: `CustomRequester → Service → Tests`. UI: `BasePage → Page Object → Tests`.
`conftest.py` в корне — фикстуры нужны всем трём наборам тестов.

## Запуск

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest -v
```

Выборочно:

```bash
pytest -m smoke          # 13
pytest -m regression     # 19, только позитивные — это не полный прогон
pytest -m negative       # 7
pytest -m ui             # 22
pytest -m cross          # 3
pytest tests/api         # 14
pytest -n 4              # параллельно
pytest -m ui --headed    # с видимым браузером
```

Allure:

```bash
pytest --alluredir=allure-results && allure serve allure-results
```

К упавшему UI-тесту автоматически прикладываются скриншот и URL страницы.

## Конфигурация

Работает без настройки. Чтобы переопределить — скопируйте `.env.example` в `.env`:
`BASE_URL`, `FRONT_URL`, `TIMEOUT`, `RETRY_ATTEMPTS`.

## CI

GitHub Actions: `lint` (ruff), `api` и `ui` smoke на каждый push/PR, полный
`regression` — ночью в 06:00 UTC и по кнопке. Allure-отчёт собирается отдельным
workflow и публикуется на GitHub Pages.
