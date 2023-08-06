# ♻️ pydwrap pydantic.BaseModel optional fields ♻️


pydwrap stores a **Option** type to implement unpacking of values if they are not **None**. The **BaseModel** is also a little extended to work with the **Option** type.


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/pydwrap.svg)](https://pypi.python.org/pypi/pydwrap)
[![versions](https://img.shields.io/pypi/pyversions/pydwrap.svg)](https://github.com/luwqz1/pydwrap)
[![license](https://img.shields.io/github/license/luwqz1/pydwrap.svg)](https://github.com/luwqz1/pydwrap/blob/main/LICENSE)


# ⭐️ A simple example ⭐️
```python
from pydwrap import BaseModel, Option


class User(BaseModel):
    """Anonim User model."""

    first_name: str
    last_name: Option[str]
    about: Option[str]
    age: Option[int]
    about: Option[str]
    city: Option[str]
    friends: list["User"]


some_response = {
    "first_name": "Max",
    "last_name": None,
    "age": None,
    "about": "Hello, World!",
    "city": None,
    "friends": [],
}
user = User(**some_response)
#> User(first_name='Max', last_name=Option(None), about=Option('Hello, World!'), age=Option(None), city=Option(None), friends=[])
print("Hello,", user.first_name + "!\n" + f"You are {user.age.unwrap(error='How old is he?')} years old.")
#> ValueError: How old is he?
```

# 📚 Documentation 📚
* In 🇷🇺 [**Russian**](https://github.com/luwqz1/pydwrap/blob/main/docs/RU.md) 🇷🇺
* In 🇺🇸 [**English**](https://github.com/luwqz1/pydwrap/blob/main/docs/EN.md) 🇺🇸