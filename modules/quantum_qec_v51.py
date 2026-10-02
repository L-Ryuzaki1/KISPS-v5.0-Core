# modules/quantum_qec_v51.py
import numpy as np
import streamlit as st

def calculate_free_energy(x_success: float, y_cns_wear: float, z_focus: float) -> float:
    """
    [ГЛАВА 9] Вычисление функции когнитивной свободной энергии F(x, y, z).
    Формализует баланс между накопленным износом и плотностью фокуса.
    """
    internal_energy = (y_cns_wear * 1.5) - (z_focus * 0.5)
    entropy_term = 20.0 * (1.0 - (x_success / 100.0))
    return round(internal_energy + entropy_term, 2)

def process_multiverse_step_v51(*args, **kwargs):
    """
    [ГЛАВА 4 / 7.5 / 8.1] Сквозной шлюз квантовой коррекции (QEC) КИСПС v5.1.
    Рассчитывает износ ЦНС, расход фокуса и синергетический буст пула миров.
    """
    # Жесткий отказоустойчивый разбор аргументов ядра
    if len(args) >= 1:
        universes = args[0]
    else:
        universes = kwargs.get("universes", [])

    if len(args) >= 2:
        step = args[1]
    else:
        step = kwargs.get("step", 1)

    num_twins = len(universes)
    if num_twins == 0:
        return universes

    is_dev_mode = st.session_state.get("manual_mode_toggle_val", False)
    
    # Распределяем параметры калибровки среды
    if is_dev_mode:
        discipline = float(st.session_state.get("dev_discipline_rate_slider_unique", 75.0))
        isolation = float(st.session_state.get("dev_isolation_v51_unique", 2.0))
        cryo_efficiency = float(st.session_state.get("dev_cryo_v51_unique", 1.5))
        s_pressure = float(st.session_state.get("dev_real_stress_slider_unique", 20.0))
    else:
        # Автономные константы гражданского режима для сохранения термодинамического баланса
        discipline = 75.0
        isolation = 2.0        
        cryo_efficiency = 1.5  
        s_pressure = 32.0  

    # Извлечение квантового потока от ANU QRNG
    quantum_stream = kwargs.get("quantum_stream", None)
    if quantum_stream is None or len(quantum_stream) < num_twins:
        quantum_stream = np.random.default_rng().random(num_twins)

    omega = 0.20  # Терагерцовое окно резонанса Стейнера
    success_values = np.array([u.get("success_value", 90.0) for u in universes if isinstance(u, dict)])
    cns_wear = np.array([u.get("cns_wear", 0.0) for u in universes if isinstance(u, dict)])
    focus = np.array([u.get("cognitive_focus", 100.0) for u in universes if isinstance(u, dict)])

    # Расчет эффекта квантового домино (перегрев пула миров)
    high_wear_ratio = sum(1 for c in cns_wear if c > 70.0) / num_twins
    domino_factor = 1.0 + (high_wear_ratio * 1.8)

    for idx in range(num_twins):
        u = universes[idx]
        if not isinstance(u, dict):
            continue

        if u.get("step_collapsed") is not None or u.get("collapsed") is True:
            u["success_value"] = 0.0
            u["cns_wear"] = 100.0
            continue

        # Преобразование потока в центрированный сдвиг флуктуаций вакуума [-1.0; +1.0]
        delta_q = (quantum_stream[idx] - 0.5) * 2.0
        
        e_time = 1.0 + (step * 0.10)
        gamma = 0.12 * (1.5 - (discipline / 100.0))
        
        base_cns_delta = delta_q * 26.0 if delta_q > 0 else delta_q * 12.0
        w_resonance = u.get("world_resonance", 0.5)
        
        # Модифицированное уравнение износа с учетом демпферов изоляции и крио-регенерации
        protected_delta = (base_cns_delta * w_resonance * e_time * np.exp(gamma * step) * domino_factor) / (isolation * cryo_efficiency)
        cns_wear[idx] = np.clip(cns_wear[idx] + protected_delta, 0.0, 100.0)
        
        # Расход фокуса под давлением среды
        q_val = (delta_q / 2.0) + 0.5
        focus[idx] = np.clip(focus[idx] - q_val * (5.0 + s_pressure * 0.12), 20.0, 150.0)
        
        x_coord = (focus[idx] - cns_wear[idx]) / 20.0
        success_values[idx] = (1.0 / (1.0 + np.exp(-x_coord))) * 100.0

        # Жесткий триггер фазового свала (перегорание структуры)
        if cns_wear[idx] >= 94.0 or focus[idx] <= 22.0:
            u["step_collapsed"] = step
            u["collapsed"] = True
            success_values[idx] = 0.0
            cns_wear[idx] = 100.0
            u["qec_status"] = "COLLAPSED: CNS Burnout"
            continue

        status = "Nominal"

        # Контур многоагентного QEC-резонанса Стейнера (восстановление по матрице смежности)
        if cns_wear[idx] > 75.0 and success_values[idx] < 35.0:
            diffs = np.abs(success_values - success_values[idx])
            coherence_matrix = np.maximum(0.0, 1.0 - (diffs / omega))
            global_syndrome = float(np.mean(coherence_matrix))
            
            if global_syndrome > 0.12:
                correction_factor = 1.0 - (discipline / 100.0) * 0.45 * global_syndrome
                cns_wear[idx] *= correction_factor
                x_coord = (focus[idx] - cns_wear[idx]) / 20.0
                success_values[idx] = max((1.0 / (1.0 + np.exp(-x_coord))) * 100.0, 45.0 + (discipline * 0.25))
                status = "QEC: Steiner Correction Applied"

        # Фиксация обновленного вектора состояния
        u["cns_wear"] = float(cns_wear[idx])
        u["success_value"] = float(success_values[idx])
        u["cognitive_focus"] = float(focus[idx])
        u["free_energy"] = calculate_free_energy(u["success_value"], u["cns_wear"], u["cognitive_focus"])
        u["qec_status"] = status
        
        if "3d_history" in u and isinstance(u["3d_history"], list):
            u["3d_history"].append((u["success_value"], u["cns_wear"], u["cognitive_focus"]))

    # Синхронизация глобальной статистики с интерфейсом
    total_collapsed = sum(1 for single_u in universes if isinstance(single_u, dict) and single_u.get("collapsed") is True)
    total_high_wear = sum(1 for single_u in universes if isinstance(single_u, dict) and single_u.get("cns_wear", 0) > 70.0 and not single_u.get("collapsed"))
    
    st.session_state["kisps_stats_nominal"] = num_twins - total_collapsed - total_high_wear
    st.session_state["kisps_stats_collapsed"] = total_collapsed
    st.session_state["kisps_stats_high_wear"] = total_high_wear

    return universes
