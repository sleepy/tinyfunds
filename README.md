## How to setup virtual enviroment

First time setup:

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt

After it's setup and you want to work on the project, you only need to reactivate it:

    source env/bin/activate

## How to run the app locally:

    python manage.py migrate
    python manage.py runserver
