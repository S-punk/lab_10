import random
import numpy as np
import matplotlib.pyplot as plt

# Функция Растригина
def fitness_function(x):
    return 10 + x**2 - 10 * np.cos(2 * np.pi * x)

# Описание пчелы
class Bee:
    def __init__(self, position):
        self.position = position  # Позиция в пространстве решений
        self.fitness = fitness_function(position)  # Значение фитнес-функции

# Алгоритм роя пчел
def bee_colony_optimization(num_bees, max_iter, lower_bound, upper_bound):
    # Инициализация пчел
    bees = [Bee(random.uniform(lower_bound, upper_bound)) for _ in range(num_bees)]
    best_bee = min(bees, key=lambda bee: bee.fitness)  # Начальный лучший результат
    
    # Для визуализации
    best_fitness_history = []
    positions_history = []
    
    for iteration in range(max_iter):
        for bee in bees:
            # Локальный поиск: случайное изменение позиции пчелы
            new_position = bee.position + random.uniform(-1, 1)  # Отклонение
            new_position = max(lower_bound, min(upper_bound, new_position))  # Ограничение
            new_fitness = fitness_function(new_position)
            
            if new_fitness < bee.fitness:
                bee.position = new_position
                bee.fitness = new_fitness
        
        # Глобальный поиск: обмен информацией между пчелами
        best_neighborhood_bee = min(bees, key=lambda bee: bee.fitness)
        if best_neighborhood_bee.fitness < best_bee.fitness:
            best_bee = best_neighborhood_bee
        
        # Сохранение данных для визуализации
        best_fitness_history.append(best_bee.fitness)
        positions_history.append([bee.position for bee in bees])
        
        print(f"Iteration {iteration + 1}: Best fitness = {best_bee.fitness}, Best position = {best_bee.position}")
    
    return best_bee.position, best_bee.fitness, best_fitness_history, positions_history

# Визуализация
def plot_optimization_process(lower_bound, upper_bound, best_fitness_history, positions_history):
    x = np.linspace(lower_bound, upper_bound, 500)
    y = fitness_function(x)
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # График фитнес-функции
    ax[0].plot(x, y, label="Fitness Function")
    ax[0].set_title("Fitness Function and Bee Positions")
    ax[0].set_xlabel("Position")
    ax[0].set_ylabel("Fitness")
    
    # График изменения лучшего фитнеса
    ax[1].plot(range(1, len(best_fitness_history) + 1), best_fitness_history, label="Best Fitness", color="orange")
    ax[1].set_title("Best Fitness Over Iterations")
    ax[1].set_xlabel("Iteration")
    ax[1].set_ylabel("Best Fitness")
    
    # Анимация позиций пчел
    for iteration, positions in enumerate(positions_history):
        ax[0].scatter(positions, [fitness_function(pos) for pos in positions], color="red", alpha=0.5, label="Bees" if iteration == 0 else "")
    
    ax[0].legend()
    ax[1].legend()
    plt.tight_layout()
    plt.show()

# Параметры
num_bees = 20  # Число пчел
max_iter = 50  # Число итераций
lower_bound = -5.12  # Нижняя граница поиска
upper_bound = 5.12  # Верхняя граница поиска

# Запуск алгоритма
best_position, best_fitness, best_fitness_history, positions_history = bee_colony_optimization(
    num_bees, max_iter, lower_bound, upper_bound
)

# Визуализация процесса оптимизации
plot_optimization_process(lower_bound, upper_bound, best_fitness_history, positions_history)

print(f"Optimal position: {best_position}, Optimal fitness: {best_fitness}")
