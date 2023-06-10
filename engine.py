"""
Движок модели Life по Conway.
Поле размером WIDTH x HEIGHT, квадратные клетки.
Живые остаются живыми, пока есть STILL_LIVE или NEW_BORN живых соседа.
Пустая клетка, окружённая NEW_BORN живыми, становится живой.
"""

from collections import defaultdict
from itertools import product
from typing import Tuple, Set, DefaultDict


WIDTH = 75
HEIGHT = 50
STILL_LIVE = 2
NEW_BORN = 3


def normalize(lives: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Сдвиг популяции к началу координат для последующего сравнения
    :param lives: множество: координаты членов популяции
    :return: множество: сдвинутые координаты
    """
    if not lives:
        return lives
    x_min = min(lives, key=lambda x: x[0])[0]
    y_min = min(lives, key=lambda x: x[1])[1]
    return set((x - x_min, y - y_min) for x, y in lives)


def milieu(central_cell: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Окружение, соседи заданной клетки
    :param central_cell: координаты клетки
    :return: множество из координат соседей
    """
    return {((central_cell[0]+i + HEIGHT) % HEIGHT, (central_cell[1]+j + WIDTH) % WIDTH)
            for i, j in product(range(-1, 2), repeat=2) if i or j}


def total_population(cells: Set[Tuple[int, int]]) -> DefaultDict:
    """
    Количество живых соседей у каждой клетки, имеющей живых соседей
    :param cells: множество: координаты живых клеток
    :return: словарь (DefaultDict): ключи - координаты клеток, значения - кол-во живых соседей
    """
    ans = defaultdict(int)
    for cell in cells:
        for m in milieu(cell):
            ans[m] += 1
    return ans


def next_step(population: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Генерация новой популяции живых Клеток
    :param population: текущая популяция
    :return: новая популяция
    """
    ans = set()
    data = total_population(population)
    for cell, val in data.items():
        if val == NEW_BORN or val == STILL_LIVE and cell in population:
            ans.add(cell)
    return ans


def generation(start: Set[Tuple[int, int]]) -> Tuple[Set[Tuple[int, int]], int]:
    """
    Генератор популяций. В финале - либо смерть, либо начало бессмертия.
    :param start: Начальная популяция.
    :return: В процессе жизни возвращает текущую популяцию и номер шага. В конце - set() плюс либо -1 (смерть),
                либо номер шага, с которого начался бесконечный цикл (бессмертие).
    """
    current, history, s = start, [set()], 0
    while True:
        if (n_c := normalize(current)) in history:
            yield set(), history.index(n_c) - 1
            return
        history.append(n_c)
        yield current, s
        current = next_step(current)
        s += 1

def infinite_generation(start: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Бесконечный генератор популяций.
    :param start: Начальная популяция.
    :return: Текущая популяция, включая возможный set().
    """
    while True:
        start = next_step(start)
        yield start
