import asyncio
import random
from sql_scripts import *


async def data_clean(data):
    result = list()
    for j in [i for i in data]:
        if j == None:
            result.append('*' + ' ❌')
        else:
            result.append(" " + j + ' ✅')

    return result[0]


async def apply_number_generation():
    uniq_numbers = get_uniq_app_number()
    while True:
        random_number = random.randint(101, 99999)
        if random_number in uniq_numbers:
            pass
        else:
            break
    return random_number


async def random_order_number_generation():
    uniq_numbers = get_uniq_order_id()
    while True:
        random_number = random.randint(10000, 99999)
        if random_number in uniq_numbers:
            pass
        else:
            break
    return random_number


async def check_twitter_link(link):
    return link.startswith("https://twitter.com/")


async def get_random_order_for_task():
    probability = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3]

    random_type = random.choice(probability)
    return random_type


async def clean_text(text, object):
    text = text.replace(object, '')
    lst = [i for i in text.split() if i != '']
    return lst[0]
