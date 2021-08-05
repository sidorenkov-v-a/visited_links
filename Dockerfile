FROM python:3.8.5

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt -U --no-deps

COPY . .

CMD bash -c \
"python manage.py wait_for_db && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
gunicorn visited_links.wsgi:application --bind 0.0.0.0:8000 --timeout 120"
