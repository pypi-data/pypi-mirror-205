# msg2bytes

MessageToBytes(msg2bytes) is an efficient binary serialization format. It lets you exchange data among multiple languages like JSON. But it's faster and smaller.

## Install

```
pip install msg2bytes
```

## Usage

```
In [1]: import datetime
   ...: import msg2bytes
   ...: 

In [2]: data1 = {
   ...:     "id": 12,
   ...:     "username": "ceshi",
   ...:     "name": "测试",
   ...:     "mobiles": ["12345678901", "12345678902"],
   ...:     "add_time": datetime.datetime(2023, 4, 25, 18, 12, 32),
   ...:     "mod_time": datetime.datetime.now(),
   ...: }

In [3]: print(data1)
{'id': 12, 'username': 'ceshi', 'name': '测试', 'mobiles': ['12345678901', '12345678902'], 'add_time': datetime.datetime(2023, 4, 25, 18, 12, 32), 'mod_time': datetime.datetime(2023, 4, 26, 13, 2, 5, 293796)}

In [4]: data2 = msg2bytes.dumps(data1)

In [5]: print(data2)
b'\x04\x06\x0b\x02id\x15\x0c\x0b\x08username\x0b\x05ceshi\x0b\x04name\x0b\x06\xe6\xb5\x8b\xe8\xaf\x95\x0b\x07mobiles\x01\x02\x0b\x0b12345678901\x0b\x0b12345678902\x0b\x08add_time\r\x132023-04-25T18:12:32\x0b\x08mod_time\r\x1a2023-04-26T13:02:05.293796'

In [6]: data3 = msg2bytes.loads(data2)

In [7]: print(data3)
{'id': 12, 'username': 'ceshi', 'name': '测试', 'mobiles': ['12345678901', '12345678902'], 'add_time': datetime.datetime(2023, 4, 25, 18, 12, 32), 'mod_time': datetime.datetime(2023, 4, 26, 13, 2, 5, 293796)}
```
## Releases

### v0.1.2

- First release.