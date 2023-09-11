# Newspaper agency


## Features
In newspaper agency app you can create Newspaper with certain topic and add or delete yourself like redactor of this topic.
Redactor can add email, first name, last name , username and years of experience.
Only admin of the page can add topics as required


## Installation

Python3 must be already installed


```shell
1. git clone https://github.com/erikagayan/newspaper-agency.git
2. python -m venv venv
3. Linux: source venv/bin/activate | Windows: .venv\Scripts\Activate.ps1
4. Change .env.example to .env:
- DJANDO_DEBUG=True (True for development, False for production)
- DJANGO_SECRET_KEY=your_DJANGO_SECRET_KEY (Put your secret key here)
- DATABASE_URL=your_DATABASE_URL (Change to your db url)
5. pip install -r requirements.txt
6. python manage.py migrate
7. python manage.py runserver
```

## git Website
[Website](https://newspaper-agency1.onrender.com)


## User
Credits
```
username: admin
password: 1qazcde3
```


## Newspaper agency DB scheme
![DB scheme](images/DB_scheme.png)


## Page example
![home](images/newspaper_agency_home.png)
![newspapers list](images/newspaper_list.png)
