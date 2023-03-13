
<a href="https://pypi.org/project/django-role/">
  <img src="https://img.shields.io/pypi/dm/django-role"/>
</a>
<a href="https://pypi.org/project/django-role/">
  <img src="https://img.shields.io/pypi/v/django-role"/>
</a>
<a href="https://github.com/isys35/django-role">
  <img src="https://img.shields.io/github/last-commit/isys35/django-role"/>
</a>
<h1>django-role</h1>


<p>Пакет включает в себя. Модель пользователя с <b>ролью</b> вместо <b>групп</b>.</p>

<p>Роль в отличии от групп связана с моделю пользователя связью <b>Один ко многим</b></p>

<h2>Установка</h2>

```pip install django-role```

```poetry add django-role```

<h3>Использование модели пользователя</h3>

<small>setting.py</small>
```python
AUTH_USER_MODEL = "user_role.User"
```
