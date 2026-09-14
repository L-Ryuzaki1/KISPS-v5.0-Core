import numpy as np

class QuantumBehavioralEngine:
    def __init__(self, discipline: float, w_resonance: float):
        """
        Инициализация ядра индивидуальной траектории.
        :param discipline: Параметр дисциплины (от 0 до 100)
        :param w_resonance: Квантовый профиль реальности
        """
        self.discipline = discipline
        self.w_resonance = w_resonance
 
    def generate_quantum_shift(self, mock_qrng_val: float = None) -> float:
        """
        Извлечение истинной случайности из флуктуаций вакуума (симуляция ANU QRNG).
        """
        q_val = mock_qrng_val if mock_qrng_val is not None else np.random.rand()
        return (q_val - 0.5) * 2.0  # Интервал [-1.0; +1.0]

    def calculate_cns_step(self, cns_wear_prev: float, delta_q: float, t: int) -> float:
        """
        Расчет прироста износа ЦНС с учетом множителя времени и фактора дисциплины.
        """
        e_time = 1.0 + (t * 0.08)
        # Асимметричный шаг: нагрузка при положительном сдвиге, восстановление при отрицательном
        delta_cns = delta_q * (24.0 if delta_q > 0 else 18.0) * self.w_resonance * e_time
        
        # Коэффициент интенсивности нарастания хаоса (замедляется дисциплиной)
        gamma = 0.12 * (1.5 - (self.discipline / 100.0))
        return max(0.0, min(100.0, cns_wear_prev + delta_cns * np.exp(gamma * t)))

    def evaluate_sigmoid_success(self, focus_prev: float, cns_wear: float, s_pressure: float, delta_q: float) -> tuple:
        """
        Расчет Квантового Бунта и логистической кривой успеха (Сигмоиды).
        """
        q_val = (delta_q / 2.0) + 0.5
        focus_new = max(50.0, min(150.0, focus_prev - q_val * (8.0 + s_pressure * 0.1)))
        
        # Вычисление когнитивного баланса
        x = (focus_new - cns_wear) / 20.0
        success_value = (1.0 / (1.0 + np.exp(-x))) * 100.0
 
        return success_value, focus_new

    def simulate_sandbox_sleep(self, cns_wear: float, b_start: float, tau_hours: float = 8.0) -> dict:
        """
        Симуляция фазы сна в изолированной "песочнице" Sandbox и дефрагментация кэша логов.
        """
        lambda_param = 0.35
        reg_eff = 1.0 - (cns_wear / 100.0)
        
        # Экспоненциальное затухание информационного хаоса в кэше логов мозга
        b_cache_end = b_start * np.exp(-lambda_param * reg_eff * tau_hours)
        cns_wear_end = max(0.0, cns_wear - 25.0 * reg_eff * (1.0 - (b_cache_end / (b_start + 1e-9))))
        
        status = "Successful Defragmentation" if (cns_wear < 90.0 and b_cache_end / (b_start + 1e-9) <= 0.5) else "Sandbox Overflow"
        return {"b_cache_final": round(b_cache_end, 2), "cns_wear_final": round(cns_wear_end, 2), "status": status}
