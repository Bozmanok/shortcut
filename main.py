import pygame as pg
from random import random
from collections import deque


print('\nРазмеры карты')
m = int(input('M (ширина) = '))
n = int(input('N (высота) = '))
print(f'Будет создано поле размером {m} на {n}\n')

print('Координаты плота')
x_raft = int(input('raft X = '))
y_raft = int(input('raft Y = '))
print(f'Плот находится на точке ({x_raft},{y_raft})\n')

print('Координаты финиша')
x_finish = int(input('finish X = '))
y_finish = int(input('finish Y = '))
print(f'Финиш находится на точке ({x_finish},{y_finish})')

# Настройки по полигону и по координатам
cols, rows = m, n
TILE = 20
start = (x_raft, y_raft)
goal = (x_finish, y_finish)


# создаём пустышку-полигон с указанными размерами
def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


# проверяем соседние клетки на границы и препятствия
def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


# поиск кратчайшего пути между плотом и целью (алгоритм обхода графа по ширине - BFS)
def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


# инициализация отображения полигона
pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])

# генерируем сетку с водой и сушей. Координаты плота и финиша помечаем как вода
grid = [[1 if random() < 0.3 else 0 for col in range(cols)] for row in range(rows)]
grid[y_raft][x_raft] = 0
grid[y_finish][x_finish] = 0

# представление сетки в виде графов
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)


while True:
    # заполняем полигон водой
    sc.fill(pg.Color('blue'))

    # прорисовка сетки с сушей на полигоне
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

    # получаем очередь вершин и словарь посещённых вершин
    queue, visited = bfs(start, goal, graph)

    # прорисовка кратчайшего пути между плотом и финишем
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
        path_segment = visited[path_segment]
    pg.draw.rect(sc, pg.Color('yellow'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)

    # выход из режима дисплея
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
