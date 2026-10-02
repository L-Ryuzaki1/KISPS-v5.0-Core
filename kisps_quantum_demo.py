# kisps_quantum_demo.py
"""
Квантово-информационный симулятор поведенческих систем (КИСПС v5.1-QuantumDemo)
Открытый академический прототип на базе симуляции квантового регистра кубитов.
© КИСПС, 2026. Разработчик: L Ryuzaki
"""
import numpy as np

class QuantumRegisterSimulation:
    """Симулятор простейшего квантового процессора для генерации энтропии."""
    @staticmethod
    def measure_hadamard_qubit() -> float:
        """
        Моделирует перевод кубита сознания в состояние суперпозиции 
        через гейт Адамара (H) и последующий акт измерения (коллапс).
        Возвращает значение флуктуации на интервале [0.0; 1.0].
        """
        # Вектор базового состояния |0>
        qubit_zero = np.array([[1.0], [0.0]], dtype=complex)
        # Матрица оператора Адамара (H-gate)
        hadamard = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
        
        # Перевод кубита в суперпозицию: |+> = H|0>
        superposition_state = np.dot(hadamard, qubit_zero)
        
        # Проекция флуктуаций фазового пространства (имитация вакуумного шума)
        phase_shift = np.random.uniform(0.0, 2.0 * np.pi)
        quantum_noise = (np.abs(superposition_state[0, 0] + np.exp(1j * phase_shift) * superposition_state[1, 0]) ** 2) / 2.0
        return float(quantum_noise)

class QuantumBehavioralEngineDemo:
    def __init__(self, discipline: float = 75.0, user_focus: float = 110.0):
        self.discipline = discipline
        self.init_focus = user_focus
        
    def run_trajectory_simulation(self, steps: int = 10) -> list:
        """Симуляция траектории цифрового двойника на основе квантовых гейтов."""
        state = {
            "success_value": 90.0,
            "cns_wear": 0.0,
            "cognitive_focus": self.init_focus,
            "status": "Nominal"
        }
        history = [dict(state)]

        for t in range(1, steps + 1):
            if state["cns_wear"] >= 94.0 or state["cognitive_focus"] <= 22.0:
                state.update({"success_value": 0.0, "cns_wear": 100.0, "status": "Burnout"})
                history.append(dict(state))
                continue

            # [ГЛАВА 3.2] Извлечение квантового сдвига из симулятора кубита
            quantum_val = QuantumRegisterSimulation.measure_hadamard_qubit()
            delta_q = (quantum_val - 0.5) * 2.0  # Интервал [-1.0; +1.0]
            
            # Параметры затухания хаоса (Дисциплина D) и экспонента Гомпертца
            e_time = 1.0 + (t * 0.10)
            gamma = 0.12 * (1.5 - (self.discipline / 100.0))
            
            base_cns_delta = delta_q * 26.0 if delta_q > 0 else delta_q * 12.0
            protected_delta = (base_cns_delta * 0.5 * e_time * np.exp(gamma * t))
            
            state["cns_wear"] = np.clip(state["cns_wear"] + protected_delta, 0.0, 100.0)
            
            # Расход когнитивного ресурса
            q_val = (delta_q / 2.0) + 0.5
            state["cognitive_focus"] = np.clip(state["cognitive_focus"] - q_val * 8.8, 20.0, 150.0)
            
            # [ГЛАВА 3.3] Вычисление логистической Сигмоиды успеха
            x_coord = (state["cognitive_focus"] - state["cns_wear"]) / 20.0
            state["success_value"] = (1.0 / (1.0 + np.exp(-x_coord))) * 100.0
            
            history.append(dict(state))
            
        return history

if __name__ == "__main__":
    engine = QuantumBehavioralEngineDemo(discipline=75.0, user_focus=110.0)
    print("--- ЗАПУСК КВАНТОВОЙ ДЕМО-СИМУЛЯЦИИ (10 ШАГОВ) ---")
    for step, data in enumerate(engine.run_trajectory_simulation()):
        print(f"Шаг {step}: Успех: {data['success_value']:.1f}% | Износ ЦНС: {data['cns_wear']:.1f}% | Статус: {data['status']}")
