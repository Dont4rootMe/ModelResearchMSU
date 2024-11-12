# Документация по бэкенду демонстрации модели для Культурного кода

**07.11.2024**

## Соглашения по бэкенду

Бэкенд поднимается в виде docker image с доступом в сеть, располагающий одним rest api endpoint – post с сигнатурой ответа:

- Вход: $str$
- Выход: $json$

Для поднятия бэкенда используется два скрпты:

* `build.sh`
* `run.sh -d path/to/model_dump -m path/to/model/api`

В дириктории `path/to/model_dump` должна лежать сохраненные веса. `path/to/model/api` находится в обязательном порядке два файла:

- `model_api.py` – пакет с фукнцией model_api
- `requirements.txt` – перечисленные для pip зависимости

Функция model_api.py имеет вид: 

``` python
def model_api(text: str):
    ...
    return {
        'entities': [{
            'start': int,
            'end': int,
            'label': str
        }],
        'text_labels': [str]
    }
```

На языке relation diagram ответ выглядит следующим образом:

``` mermaid
erDiagram
RESPONSE ||--o{ entities : has
entities ||--|| start : starts_with
entities ||--|| end : ends_with
entities ||--|| label : marked_by

RESPONSE ||--o{ text_labels: sumarizes

```

Поднимаемый сервер один раз собирается с базовыми torch библиотеками и затем при каждом развертывании подтягивает через mount нужную модель и api ее общения. 