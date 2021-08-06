import string
from datetime import datetime, timedelta, timezone
import random
from math import floor

def create_client_data(links=None):
    if links:
        return {'links': links}

    data = {
        'links': [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }
    return data


def create_data_for_db(add_seconds=0, count=3):

    date = datetime.now(timezone.utc) + timedelta(seconds=add_seconds)
    timestamp = floor(date.timestamp())

    links = []
    letters = string.ascii_lowercase
    for _ in range(count):
        domain = ''.join(random.choice(letters) for i in range(5))
        links.append({'domain': f'{domain}.com', 'date': date}, )

    return links, timestamp
