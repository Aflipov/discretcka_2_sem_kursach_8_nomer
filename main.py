import sys
import random
import os
from typing import List

class GraphAnalyzer:
    def __init__(self):
        self.adj_matrix = []
        self.sccs = []
        self.condensed = []

    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def kosaraju_scc(self, adj_matrix: List[List[int]]) -> List[List[int]]:
        """Алгоритм Косарайю для поиска компонент сильной связности"""
        n = len(adj_matrix)
        visited = [False] * n
        order = []
        sccs = []

        def dfs1(v):
            visited[v] = True
            for w in range(n):
                if adj_matrix[v][w] and not visited[w]:
                    dfs1(w)
            order.append(v)

        def dfs2(v, component):
            visited[v] = True
            component.append(v)
            for w in range(n):
                if adj_matrix_transposed[v][w] and not visited[w]:
                    dfs2(w, component)

        # Первый обход
        for v in range(n):
            if not visited[v]:
                dfs1(v)

        # Транспонируем граф
        adj_matrix_transposed = [[adj_matrix[j][i] for j in range(n)] for i in range(n)]
        
        # Второй обход
        visited = [False] * n
        for v in reversed(order):
            if not visited[v]:
                component = []
                dfs2(v, component)
                sccs.append(component)

        return sorted([sorted(comp) for comp in sccs])

    def condensation_graph(self, adj_matrix: List[List[int]], sccs: List[List[int]]) -> List[List[int]]:
        """Построение графа конденсации"""
        vertex_to_scc = {v: i for i, comp in enumerate(sccs) for v in comp}
        condensed = [[0]*len(sccs) for _ in range(len(sccs))]
        
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix)):
                if adj_matrix[i][j] and vertex_to_scc[i] != vertex_to_scc[j]:
                    condensed[vertex_to_scc[i]][vertex_to_scc[j]] = 1
        return condensed

    def generate_random_graph(self, n: int = None, density: float = None) -> List[List[int]]:
        """Генерация случайного графа"""
        if n is None:
            n = random.randint(4, 9)
        if density is None:
            density = min(0.5, max(0.2, random.random()))
        
        return [[1 if random.random() < density and i != j else 0 for j in range(n)] for i in range(n)]

    def input_graph_manually(self):
        """Ручной ввод графа"""
        self.clear_screen()
        print("=== Ручной ввод графа ===")
        
        while True:
            try:
                n = int(input("Количество вершин (2-9): "))
                if 2 <= n <= 9:
                    break
                print("Ошибка: введите число от 2 до 9")
            except ValueError:
                print("Ошибка: введите целое число")
        
        print("\nВведите матрицу смежности (построчно):")
        print(f"Пример строки: {'1 ' * n}")
        
        self.adj_matrix = []
        for i in range(n):
            while True:
                try:
                    row = list(map(int, input(f"Строка {i+1}: ").split()))
                    if len(row) != n:
                        print(f"Ошибка: требуется {n} значений")
                        continue
                    if any(x not in (0, 1) for x in row):
                        print("Ошибка: используйте только 0 и 1")
                        continue
                    self.adj_matrix.append(row)
                    break
                except ValueError:
                    print("Ошибка: введите числа через пробел")

    def show_results(self):
        """Отображение результатов анализа"""
        self.clear_screen()
        print("=== Результаты анализа ===")
        
        if not self.adj_matrix:
            print("Граф не загружен!")
            input("\nНажмите Enter чтобы вернуться...")
            return
        
        print("\nМатрица смежности графа:")
        print(f"   {" ".join([f"{i + 1}" for i in range(len(self.adj_matrix))])}")
        for i, row in enumerate(self.adj_matrix):
            print(f"{i + 1} |" + " ".join(map(str, row)) + "|")
        
        print("\nКомпоненты сильной связности:")
        for i, comp in enumerate(self.sccs):
            # print(f"Компонента {i}: вершины {comp}")
            print(f"Компонента {i + 1}: вершины {[i + 1 for i in comp]}")
        
        print("\nМатрица конденсации:")
        print(f"К  {" ".join([f"{i + 1}" for i in range(len(self.sccs))])}")
        for i, row in enumerate(self.condensed):
            print(f"{i + 1} |" + " ".join(map(str, row)) + "|")
        
        input("\nНажмите Enter чтобы вернуться...")

    def main_menu(self):
        """Главное меню"""
        while True:
            self.clear_screen()
            print("=== Анализатор графов ===")
            print("1. Ввести граф вручную")
            print("2. Сгенерировать случайный граф")
            print("3. Использовать пример из кода")
            print("4. Показать результаты анализа")
            print("5. Выход")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self.input_graph_manually()
                if self.adj_matrix:
                    self.sccs = self.kosaraju_scc(self.adj_matrix)
                    self.condensed = self.condensation_graph(self.adj_matrix, self.sccs)
                
            elif choice == "2":
                self.clear_screen()
                print("=== Генерация случайного графа ===")
                try:
                    n = int(input("Количество вершин (4-9, Enter для случайного): ") or random.randint(4, 9))
                except ValueError:
                    n = None
                
                density = None
                if n is not None:
                    try:
                        d = float(input("Плотность графа (0.1-0.5, Enter для случайной): ") or random.random())
                        if 0 < d <= 1:
                            density = d
                    except ValueError:
                        pass
                
                self.adj_matrix = self.generate_random_graph(n, density)
                print("\nСгенерирован граф:")
                print(f"   {" ".join([f"{i + 1}" for i in range(len(self.adj_matrix))])}")
                for i, row in enumerate(self.adj_matrix):
                    print(f"{i + 1} |" + " ".join(map(str, row)) + "|")
                
                # for row in self.adj_matrix:
                #     print(" ".join(map(str, row)))
                
                self.sccs = self.kosaraju_scc(self.adj_matrix)
                self.condensed = self.condensation_graph(self.adj_matrix, self.sccs)
                input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == "3":
                self.adj_matrix = [
                    [0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0]
                ]
                print("Использован тестовый граф:")
                print(f"   {" ".join([f"{i + 1}" for i in range(len(self.adj_matrix))])}")
                for i, row in enumerate(self.adj_matrix):
                    print(f"{i + 1} |" + " ".join(map(str, row)) + "|")
                
                self.sccs = self.kosaraju_scc(self.adj_matrix)
                self.condensed = self.condensation_graph(self.adj_matrix, self.sccs)
                input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == "4":
                if self.adj_matrix:
                    self.show_results()
                else:
                    print("Сначала загрузите граф!")
                    input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == "5":
                self.clear_screen()
                print("Программа завершена.")
                sys.exit(0)
                
            else:
                print("Неверный выбор!")
                input("\nНажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    analyzer = GraphAnalyzer()
    analyzer.main_menu()