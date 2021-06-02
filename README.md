# Проект

Бот здесь:  [https://t.me/turtlecoin_bot](https://t.me/turtlecoin_bot)

# Turtlecoin API Async Daemon

## Соединение


## Запуск сервиса
```
trtl = await turtlecoin.wallet(connect_cons, {"filename": "mywallet.wallet", "password":"123456"}).start()
```

`.start()` запускает wallet-api

Для тех у кого Windows я приму ваши доработки в git :)

Для запуска сервиса передайте путь к исполняемому файлу `"cmd": "/путь_к_файлу/wallet-api"`
## Метод WALLET

Для передачи параметров соединения используем `dict` (словарь), переменную назовем `connect_cons` (см. примеры)

Второй аргумент передайте словарь.
Пример:
`{"filename": "mywallet.wallet", "password":"123456"}`

### Импорт
**Импорт кошелька вызывать после вызова метода `import_()`**

Импортировать кошелек можно по фразе, по ключу (это ключи `privateViewKey`, `privateSpendKey`)

В `import_()` можно передать параметр `scanHeight`

**БЕЗОПАСТНОСТЬ: Не сообщайте НИКОМУ свою фразу из 25 слов, а так же `privateViewKey` и `privateSpendKey` вы потеряете деньги**

### Создание кошелька
**!!! Обратите внимание метод wallet имеет обязательные ключи в словаре это `filename`, `password`**
Пример:
```
import asyncio
from turtlecoin_api as turtlecoin

connect_cons = {"server": "http://127.0.0.1:8181", "password": "Dy6566rgygt6g", "timeout": "5"}

async def asynchronous():
    trtl = turtlecoin.wallet(connect_cons, {"filename": "mywallet.wallet", "password":"123456"})
    await trtl.create_() # Вызываем метод для создания кошелька

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.run_forever()
```

## Схема
```
turtlecoin
└ wallet(connect, param -> {filename, password}).start()
 ├ .open()
 ├ .create()
 ├ .close()
 ├ .import_(scanHeight -> int).seed(mnemonic -> str or list)
 ├ .import_(scanHeight -> int).key(privateViewKey and privateSpendKey)
 ├ .import_(scanHeight -> int).view(privateViewKey and address)
```
**UPDATE: Проект находится еще в разработке**
### Ошибки:
Для отключения режима отладки установите ключ `"debug": False`

Пример:
```
connect_cons = {"server": "http://127.0.0.1:8181", "password": "Dy6566rgygt6g", "timeout": "5", "debug": False}
```

ERROR: Missing wallet "filename" or "password"

Установка кастомной ноды должна быть после метода создание, импорта.

**Task was destroyed but it is pending!**
Объект не держится в памяти используйте
`ioloop.run_forever()`
либо используйте список или словарь для помещения объекта в память, простыми словами программа завершается не успев подгрузить нужное

**UPDATE: Проект находится еще в разработке**

## Установка проекта
```
git clone https://github.com/big-vl/turtlecoin
python3.9 -m pip install pipenv
sudo apt install zbar-tools
pipenv install -d --pre
pipenv shell
nano .env
```

### Установите переменные:
```
TG_SESSION="bot"
TG_API_ID=123456
TG_API_HASH="hash"
TG_TOKEN="id:hash"
```

### Запуск бота
`python3.9 run.py`
