# simple-spider-tool17

----

[simple-spider-tool](https://pypi.org/project/simple-spider-tool/) `0.0.18`及后续版本兼容之前版本使用的可选扩展包

## 安装
```shell
pip install simple-spider-tool[seventeen]
```

## 简单使用

```python
from simple_spider_tools import format_json, jsonpath

data = {
    "code": 200,
    "data": [
        {
            "id": 1,
            "username": "admin",
            "level": "boss"
        },
        {
            "id": 2,
            "username": "user",
            "level": "staff"
        }
    ]
}

boss_name = jsonpath(data, '$.data[?(@.level=="boss")].username', first=True)
all_user_info = jsonpath(data, '$.data[*].username')

print(boss_name)
print(format_json(all_user_info))
```