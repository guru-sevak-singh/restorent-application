### Create a virtual environment & install dependencies
1. python -m venv venv
2. source venv/bin/activate   # Mac/Linux
3. venv\Scripts\activate      # Windows
4. pip install -r requirements.txt


### Configure PostgreSQL in settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



### Run migrations & start server
1. python manage.py migrate
2. python manage.py runserver


### Open in browser
url - http://127.0.0.1:8000/