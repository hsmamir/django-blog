# django-blog

1. copy `sample.env` to `.env`
2. activate pip environment and install dependencies
   - run `pipenv shell`
   - run `pipenv sync -d`
3. run Django project
   - `./manage.py migrate`
   - `./manage.py runserver`
4. open your browser and go to http://127.0.0.1:8000/swagger/
