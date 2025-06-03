import time
import random
from collections import deque
from queue import LifoQueue


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.n = len(maze)
        self.m = len(maze[0]) if self.n > 0 else 0
        self.visited = [[False for _ in range(self.m)] for _ in range(self.n)]

    def reset_visited(self):
        self.visited = [[False for _ in range(self.m)] for _ in range(self.n)]

    def get_entrances(self):
        entrances = []
        if self.n == 0:
            return entrances
        for j in range(self.m):
            if self.maze[0][j] == 0:
                entrances.append((0, j))
        return entrances

    def get_exits(self):
        exits = []
        if self.n == 0:
            return exits
        for j in range(self.m):
            if self.maze[self.n - 1][j] == 0:
                exits.append((self.n - 1, j))
        return exits

    def is_valid(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.m and self.maze[x][y] == 0 and not self.visited[x][y]

    # Реализация DFS с использованием стека на массиве
    def find_path_array_stack(self, start, end):
        if not self.is_valid(start[0], start[1]) or not self.is_valid(end[0], end[1]):
            return False

        self.reset_visited()
        stack = []
        stack.append((start[0], start[1], []))

        while stack:
            x, y, path = stack.pop()
            if (x, y) == end:
                return True

            if self.visited[x][y]:
                continue

            self.visited[x][y] = True

            # Добавляем соседей в стек
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    stack.append((nx, ny, path + [(x, y)]))

        return False

    # Реализация DFS с использованием стека на связанном списке
    def find_path_linked_list_stack(self, start, end):
        if not self.is_valid(start[0], start[1]) or not self.is_valid(end[0], end[1]):
            return False

        self.reset_visited()
        stack = deque()
        stack.append((start[0], start[1], []))

        while stack:
            x, y, path = stack.pop()
            if (x, y) == end:
                return True

            if self.visited[x][y]:
                continue

            self.visited[x][y] = True

            # Добавляем соседей в стек
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    stack.append((nx, ny, path + [(x, y)]))

        return False

    # Реализация DFS с использованием стека из стандартной библиотеки
    def find_path_std_stack(self, start, end):
        if not self.is_valid(start[0], start[1]) or not self.is_valid(end[0], end[1]):
            return False

        self.reset_visited()
        stack = LifoQueue()
        stack.put((start[0], start[1], []))

        while not stack.empty():
            x, y, path = stack.get()
            if (x, y) == end:
                return True

            if self.visited[x][y]:
                continue

            self.visited[x][y] = True

            # Добавляем соседей в стек
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    stack.put((nx, ny, path + [(x, y)]))

        return False

    # Решение задачи (a) - каждый человек идет к своему выходу
    def solve_a(self, stack_type='array'):
        entrances = self.get_entrances()
        exits = self.get_exits()
        k = min(len(entrances), len(exits))

        if k == 0:
            return False

        # Для каждого входа ищем путь к соответствующему выходу
        for i in range(k):
            start = entrances[i]
            end = exits[i]

            if stack_type == 'array':
                found = self.find_path_array_stack(start, end)
            elif stack_type == 'linked_list':
                found = self.find_path_linked_list_stack(start, end)
            else:
                found = self.find_path_std_stack(start, end)

            if not found:
                return False

        return True

    # Решение задачи (b) - люди могут выходить через любой выход
    def solve_b(self, stack_type='array'):
        entrances = self.get_entrances()
        exits = self.get_exits()
        k = len(entrances)

        if k == 0 or len(exits) == 0:
            return False

        # Для каждого входа ищем путь к любому выходу
        for i in range(k):
            start = entrances[i]
            found = False

            for end in exits:
                self.reset_visited()

                if stack_type == 'array':
                    path_found = self.find_path_array_stack(start, end)
                elif stack_type == 'linked_list':
                    path_found = self.find_path_linked_list_stack(start, end)
                else:
                    path_found = self.find_path_std_stack(start, end)

                if path_found:
                    found = True
                    break

            if not found:
                return False

        return True


def generate_random_maze(n, m, wall_prob=0.3):
    maze = [[1 if random.random() < wall_prob else 0 for _ in range(m)] for _ in range(n)]

    # Гарантируем хотя бы один вход и выход
    for j in range(m):
        if maze[0][j] == 1 and random.random() < 0.5:
            maze[0][j] = 0
        if maze[n - 1][j] == 1 and random.random() < 0.5:
            maze[n - 1][j] = 0

    return maze


def test_performance():
    # Генерируем один случайный размер лабиринта от 1 до 1000
    n, m = random.randint(1, 100), random.randint(1, 100)
    print(f"Тестируем лабиринт размером {n}x{m}")

    # Генерируем лабиринт
    maze = generate_random_maze(n, m)
    solver = MazeSolver(maze)

    # Проверяем количество входов и выходов
    entrances = solver.get_entrances()
    exits = solver.get_exits()
    print(f"Найдено входов: {len(entrances)}, выходов: {len(exits)}")

    if not entrances or not exits:
        print("Не найдено входов или выходов, тестирование невозможно")
        return

    # Сравниваем производительность для каждой реализации стека
    stack_types = ['array', 'linked_list', 'std']
    results = {'a': {}, 'b': {}}

    for stack_type in stack_types:
        print(f"\nТестируем реализацию стека: {stack_type}")

        # Тестируем задачу (a)
        start_time = time.time()
        result_a = solver.solve_a(stack_type)
        time_a = time.time() - start_time
        results['a'][stack_type] = (result_a, time_a)
        print(f"Задача (а) - свой выход для каждого: результат={'Да' if result_a else 'Нет'}, время={time_a:.6f}с")

        # Тестируем задачу (b)
        start_time = time.time()
        result_b = solver.solve_b(stack_type)
        time_b = time.time() - start_time
        results['b'][stack_type] = (result_b, time_b)
        print(f"Задача (б) - любой выход подходит: результат={'Да' if result_b else 'Нет'}, время={time_b:.6f}с")

    # Выводим сравнительные результаты
    print("\nСравнительные результаты:")
    print("\nЗадача (а) - каждый человек к своему выходу:")
    for stack_type in stack_types:
        result, t = results['a'][stack_type]
        print(f"{stack_type:12s}: {'Да' if result else 'Нет'}, время = {t:.6f}с")

    print("\nЗадача (б) - можно использовать любой выход:")
    for stack_type in stack_types:
        result, t = results['b'][stack_type]
        print(f"{stack_type:12s}: {'Да' if result else 'Нет'}, время = {t:.6f}с")


if __name__ == "__main__":
    random.seed(42)  # Для воспроизводимости результатов
    test_performance()