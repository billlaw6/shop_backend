import random


def _generate_order_no():
    order_no = ''
    characters = '123456789ABCDEFG'
    order_no_length = 20
    for c in range(order_no_length):
        order_no += characters[random.randint(0, len(characters) - 1)]
    return order_no
