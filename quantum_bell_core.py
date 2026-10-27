import numpy as np

class QuantumBellEngine:
    """
    Модуль квантовой игры Белла для ядра КИСПС.
    Отвечает за расчет квантово-коррелированных исходов и коэффициентов 
    для многоагентной системы без засорения основного цикла симуляции.
    """
    def __init__(self, alpha: float = np.pi / 4):
        # Базовый квантовый параметр (фазовый сдвиг / угол волновой функции)
        self.alpha = alpha

    def _calculate_quantum_probabilities(self, strategy_a: np.ndarray, strategy_b: np.ndarray) -> np.ndarray:
        """
        Внутренний математический расчет вероятностей на основе нарушений неравенств Белла.
        Принимает векторы стратегий (0 или 1) и возвращает квантовый коэффициент корреляции.
        """
        # Симуляция тригонометрической зависимости квантовых исходов (косинус угла измерений)
        angle_diff = self.alpha * (strategy_a - strategy_b)
        
        # Квантовый коэффициент совпадения (от -1 до 1)
        quantum_correlation = np.cos(2 * angle_diff)
        return quantum_correlation

    def evaluate_agents_interaction(self, correlation_matrix: np.ndarray) -> np.ndarray:
        """
        Публичный API для ядра. Принимает матрицу или вектор текущих состояний агентов,
        применяет к ней квантовую модификацию Белла и возвращает измененные веса влияния.
        """
        # Превращаем классические веса в квантовые вероятности исходов
        # Ограничиваем clip'ом, чтобы не выйти за пределы физических вероятностей [0.0, 1.0]
        quantum_modifiers = np.clip((correlation_matrix + np.sin(self.alpha)) / 2.0, 0.0, 1.0)
        return quantum_modifiers

    def get_bell_distribution(self, size: int) -> np.ndarray:
        """
        Генерация квантового шума Белла для распределения энергии/флуктуаций агентов.
        Использует волновое смещение, обусловленное квантовым нарушением.
        """
        # Симуляция квантового распределения через суперпозицию двух фаз
        phase_1 = np.random.normal(0, 1, size)
        phase_2 = np.cos(self.alpha) * np.random.normal(0, 1, size)
        
        # Результирующий волновой профиль распределения
        bell_noise = (phase_1 + phase_2) / np.sqrt(2)
        return bell_noise
