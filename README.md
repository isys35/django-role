
<a href="https://pypi.org/project/django-role/">
  <img src="https://img.shields.io/pypi/dm/django-role"/>
</a>
<a href="https://pypi.org/project/django-role/">
  <img src="https://img.shields.io/pypi/v/django-role"/>
</a>
<a href="https://github.com/isys35/django-role">
  <img src="https://img.shields.io/github/last-commit/isys35/django-role"/>
</a>

# django-role

Пакет включает в себя:
* Модель пользователя с **ролью** вместо **групп**
* Виджет для выбора прав

Роль в отличии от групп связана с моделю пользователя связью **Один ко многим**

## Установка

```pip install django-role```

```poetry add django-role```

### Использование модели пользователя

_setting.py_
```python
AUTH_USER_MODEL = "user_role.User"
```
