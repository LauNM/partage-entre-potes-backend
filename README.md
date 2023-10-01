## Install project

copy .env.example and change name to .env.

add email host user and email host password

Generate secret key:
```bash
python3 manage.py shell

from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```


create .venv

```bash
 python3 -m venv .venv
```

## Launch virtual environment

```bash
 . .venv/bin/activate
```

## Install dependencies

```bash
 pip install -r requirements.txt 
```

## run project

```bash
. .venv/bin/activate

python3 manage.py runserver
```
