""" Модуль містить функції для створення списку випадкового згенерованих строк
Довжина строки, кількість елементів, ім'я файлу для збереження списку визначається константами
"""
import random
import string
from typing import List

# довжина строки
LEN_STR = 15
# кількість строк у списку
ITEM_COUNT = 5_000_000
# ім'я файлу, у який зберігається список
FILE_NAME='test_set.txt'

def generate_random_string(length: int) -> str:
    """
    :param length: довжина строки
    :return: строка
    Функція повертає випадково згенеровану строку доживною length
    """
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def generate_list_random_str(size: int) -> List[str]:
    """

    :param size:
    :return:
    Функція створює список, який містить строки, створені функцією generate_random_string.
        """
    list_str=[]
    for i in range(size):
        list_str.append(generate_random_string(LEN_STR))
    return list_str

def save_list_to_file(fname: str, in_list: List[str]) -> None:
    """

    :param fname: ім'я файлу
    :param in_list: список строк
    :return: None
    Функція зберігає список строк у файл
    """
    with open(fname,mode='w') as f:
        f.writelines('\n'.join(in_list))

def read_list_from_file(fname: str) -> List[str]:
    """

    :param fname: ім'я файлу
    :return: список строк
    Функція читає список строк із файлу
    """
    out_list=[]
    with open(fname, mode='r') as f:
        for line in f:
            out_list.append(line.replace('\n', ''))

    return out_list

if __name__ == '__main__':
    rnd_list= generate_list_random_str(ITEM_COUNT)
    rnd_list.sort()
    save_list_to_file(FILE_NAME, rnd_list)
    rnd_list=read_list_from_file(FILE_NAME)
    pass










