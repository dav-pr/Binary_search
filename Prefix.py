""" Модуль реалізує набір класів для використання бінарного пошуку для вирішення різноманітних задач
"""

from abc import ABC, abstractmethod
import enum
from multiprocessing import Process, Value
from threading import Thread
from typing import List, Union
from testset import read_list_from_file, FILE_NAME

class Param(enum.Enum):
    """
    Клас реалізує константи

    right - пошук правого інтервала
    left - пошук лівого інтервала
    """
    right = -1
    left = 1


class Result(enum.Enum):
    """
    notfind - елемент  не знайдений
    """
    notfind = -1


class BinarySearch(ABC):
    """
    Абстрактний клас BinarySearch являє собою загальний концепт реалізації бінарного пошуку.
    Клас BinarySearch містить такі методи:
        binary_search_engine - алгоритм бінарного пошуку у відсортованому масиві, який спирається на такі методи:
        is_find, який визначає, що елемент знайдено, та метод
        is_lower, який реалізовує алгоритм порівняння елементів.

    """

    def binary_search_engine(self, in_list: List, looking_item, start: int, end: int, *args) -> Union[int, Result]:
        """

        :param in_list: відсортований список
        :param looking_item: елемент, який шукається
        :param start: індекс початку пошуку
        :param end: індекс завершення пошуку
        :param *args - інші аргументи, які можуть передаватись функції
        :return: Union[int, Result.notfind]

        Метод являє собою класичну реалізацію бінарного пошуку. Вхідний список має бути відсортований, це є необхідною
        умовою застосування алгоритму бінарного пошуку. Список може містити елементи будь-якого типу, оскільки логічні
        операції порівняння елементов винесені в окремі методи: is_find та is_lower.
        Метод повертає індекс елементу looking_item у масиві in_list, або значення Result.notfind, якщо список не
        містить такого елементу

        """
        if start > end:
            return Result.notfind
        mid = (start + end) // 2
        idx_find = self.is_find(in_list, mid, looking_item, *args)
        if not isinstance(idx_find, Result):
            return idx_find
        if self.is_lower(in_list, mid, looking_item, *args):
            return self.binary_search_engine(in_list, looking_item, start, mid - 1, *args)
        else:
            return self.binary_search_engine(in_list, looking_item, mid + 1, end, *args)

    @abstractmethod
    def is_lower(self, in_list: List, mid: int, looking_item, *args) -> bool:
        """

        :param in_list: Список елементів. Вхідний список має бути відсортований, це є необхідною
        умовою застосування алгоритму бінарного пошуку. Список може містити елементи будь-якого типу
        :param mid: індекс елементу, який порівнується
        :param looking_item: елемент, який шукається
        :param *args - інші аргументи, які можуть передаватись функції
        :return: повертає результат порівняння - True або False


        Абстрактний метод, який повинен містити реалізацію логічної функції "<" для порівняння елементів масиву або умов
        пошуку елементу (елементів масиву).
        """
        ...

    @abstractmethod
    def is_find(self, in_list: List, mid: int, looking_item, *args) -> bool:
        """

        :param in_list: Список елементів. Вхідний список має бути відсортований, це є необхідною
        умовою застосування алгоритму бінарного пошуку. Список може містити елементи будь-якого типу
        :param mid: індекс елементу, який порівнується
        :param looking_item: елемент, який шукається
        :return: повертає результат порівняння - True або False

        Абстрактний метод, який повинен містити реалізацію логічної функції "==" для порівняння елементів масиву
        або умов пошуку елементу (елементів масиву).
        """
        ...


class BinarySearchPrefix(BinarySearch):
    """
        Клас та його методи призначені для вирішення такої задачі: Заданий відсортований масив
    строк. Необхідно знайти індекси першого і останнього елемента у послідовності елементів
    масиву, які починаються на заданий префікс.
        BinarySearchPrefix  є класом-нащадком класу BinarySearch, оскільки вирішення задачи грунтується
    на бінарному пошуку.
        Алгоритм вирішення задачі наступний: отримуємо середній елемент вхідного масиву. На наступному
    кроці алгоритму отримуємо та аналізуємо один елимент справа та зліва від середнього. Таким чином,
    отримуємо послідовність із трьох елементів. Водночас, середній елемент може бути крайнім у списку,
    тобто чи першім чи останнім. У такому випадку відсутність сусідного елемента буде позначатися як
    None. Тобто можливі такі варіанти послідності трьох елементів:
    [None|str, str, None|str].
        Першій елемент послідовності, що починається на заданий префікс, повинен ліворуч мати або None, або
    строку, яка не містить префіксу. Останній елемент такої послідовності повинен мати таку умову ліворуч.
    Тобто на наступному кроці алгоритму, після отримання " середнього" елементу та сусідніх необхідно
    перевірити наявність таких умов.


    """

    @staticmethod
    def get_safety_neighborhoods(in_list: List[str], mid: int) -> Union[int, None]:
        """
       :param in_list: список відсортованих строк
       :param mid:  індекс елемента
       :return: індекс сусідніх до mid елементів. Якщо сусіднього елемента немає повертається None
       Метод безпечно повертає індекси сусідніх елементів.
       Якщо сусіднього елемента немає повертається None.

       """

        if isinstance(mid, int):
            if mid < 0 or mid > len(in_list) - 1:
                raise ValueError
            else:
                item_left = in_list[mid - 1:mid]
                idx_left = mid - 1
                if len(item_left) == 0:
                    idx_left = None

                item_right = in_list[mid + 1:mid + 2]
                idx_right = mid + 1
                if len(item_right) == 0:
                    idx_right = None

                return idx_left, idx_right
        else:
            return None, None

    def is_find(self, in_list: List[str], mid: int, prefix: str, side: Param) -> Union[int, Result]:
        """

        :param in_list: список відсортованих строк
        :param mid: індекс елемента
        :param prefix: префікс
        :param side: ознака того чи здійснюється пошук лівої чи правої межі послідовності, яка починається
        на префікс
        :return:  повертає або індекс початку або закінчення послідності строк, яка  починається
        на префікс, або Result.notfind - у випадку, якщо не знайдено початок або закінчення такої
        послідовності
        """
        idx_left, idx_right = self.get_safety_neighborhoods(in_list, mid)
        flag = False
        element = [idx_left, mid, idx_right]
        if side == Param.right:
            element = element[::-1]
        for idx in element:
            if idx is None or not in_list[idx].startswith(prefix):
                flag = True
            else:
                if in_list[idx].startswith(prefix) and flag:
                    return idx
                else:
                    return Result.notfind
        return Result.notfind

    def is_lower(self, in_list: List[str], mid: int, pref: str, side: Param) -> bool:
        """

        :param in_list: список відсортованих строк
        :param mid: індекс елемента
        :param pref: префікс
        :param side:  ознака пошуку лівої чи правої межі послідовності, яка починається
        на префікс
        :return: повертає True або False. Значення, що повертається визначає поведінку алгоритму бінарного пошуку,
        тобто напрямок руху алгоритму - праворуч чи ліворуч від середнього елементу.
        """

        if (pref < in_list[mid] and side == Param.left) or \
                (pref < in_list[mid] and side == Param.right and not in_list[mid].startswith(pref)):
            return True
        else:
            return False

    def print_neighborhoods(self, in_list: List[str], mid: int):
        """

        :param in_list: список відсортованих строк
        :param mid: індекс елементу списку
        :return:
        Метод виводить у консоль сусідні для елементу з індексом mid елементи.
        Метод може бути використаний для ручного тестування результатів роботи алгоритму.
        Користувач візуально може переконатися, що індекси початку і закінчення послідовності знайдені вірно.
        Такий спосіб виведення інформації корисний, коли список строк дуже об'ємний і виводити усю послідовність
        у консоль не зручно
        """
        if mid is not None or not isinstance(mid, Result):
            idx_r, idx_l = self.get_safety_neighborhoods(in_list, mid)
            print('...')
            for idx in [idx_r, mid, idx_l]:
                if idx != None:
                    print(f'idx={idx}', f"list[{idx}] = {in_list[idx]}")
            print('...')
        else:
            print(None)

    def find_prefix(self, in_list: List[str], prefix: str) -> tuple:
        """

        :param in_list: список відсортованих строк
        :param prefix: префікс
        :return:  кортеж індексів, який відповідає початку послідовності елементів списку з префіксом prefix
        та його закінченням. Якщо така послідовність не знайдена, то повертається кортеж з  Result.notfind

        Метод послідовно здійснює пошук лівого та правого елементів списку з префіксом prefix.
        """
        idx_left = self.binary_search_engine(in_list, prefix, 0, len(in_list) - 1, Param.left)
        if not isinstance(idx_left, Result):
            if idx_left == len(in_list) - 1:
                idx_right = idx_left
            else:
                idx_right = self.binary_search_engine(in_list, prefix, idx_left + 1, len(in_list) - 1, Param.right)
            return idx_left, idx_right

        else:
            return Result.notfind, Result.notfind


class BinarySearchPrefixMultiProcessing():
    """
    Клас реалізує вирішення задачі з пошуку   індексів, які відповідають початку послідовності елементів списку
    з префіксом prefix та його закінченням,  з використанням технології multiprocessing
    """

    def __init__(self):
        self.bs = BinarySearchPrefix()

    def create_flow(self, targ, *args):
        return Process(target=targ, args=(args))


    def binary_search_engine(self, in_list: List, pref, start, end, side: Param, v: Value) -> None:
        """

        :param in_list: список відсортованих строк
        :param pref: префікс
        :param start: початок діапазону пошуку
        :param end: закічення діапазону пошуку
        :param side: ознака напрямау пошуку (зліва чи справа)
        :param v: (знайдений індекс )
        :return: None
        """
        res = self.bs.binary_search_engine(in_list, pref, start, end, side)
        if isinstance(res, int):
            v.value = res
        else:
            v.value = Result.notfind.value

    def find_prefix(self, in_list: List[str], prefix: str) -> tuple:
        """

        :param in_list: список відсортованих строк
        :param prefix: префікс
        :return:
        Вирішення задачі з пошуку   індексів, які відповідають початку послідовності елементів списку
        з префіксом prefixт та його закінченням,  з використанням технології multiprocessing
        """

        self.idx_left = Value('i')
        process_left = self.create_flow(self.binary_search_engine, in_list, prefix, 0, len(in_list) - 1, Param.left,
                                        self.idx_left)

        self.idx_right = Value('i')
        process_right = self.create_flow(self.binary_search_engine, in_list, prefix, 0, len(in_list) - 1, Param.right,
                                         self.idx_right)

        process_left.start()
        process_right.start()

        while process_left.is_alive() or process_right.is_alive():
            continue

        return self.idx_left.value, self.idx_right.value

class BinarySearchPrefixMultiThreding(BinarySearchPrefixMultiProcessing):
    """
    Клас реалізує вирішення задачі з пошуку   індексів, які відповідають початку послідовності елементів списку
    з префіксом prefix та його закінченням,  з використанням технології multiprocessing
    """

    def __init__(self):
       super().__init__()

    def create_flow(self, targ, *args):
        return Thread(target=targ, args=(args))


if __name__ == '__main__':
    pass
