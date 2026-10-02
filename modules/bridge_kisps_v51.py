# modules/bridge_kisps_v51.py
import os
import numpy as np
import streamlit as st
import importlib

def run_isolated_simulation_v51(engine, steps_count, user_discipline, isolation, cryo_efficiency):
    """
    [ГЛАВА 7.5] Движок-перехватчик КИСПС v5.1 для исключения интерференции логов.
    Изолирует волновой пакет и транслирует истинную случайность ANU QRNG строго 1 раз за такт.
    """
    num_twins = engine.num_universes
    is_dev = st.session_state.get("manual_mode_toggle_val", False)
    user_focus = st.session_state.get("dev_focus_boost_slider_unique", 110.0) if is_dev else 75.0
    
    universes = []
    detailed_tracks = [[] for _ in range(num_twins)]
    quantum_matrix, source_logs = [], []
    
    # Инициализация чистых профилей Мультивселенной v5.1
    for _ in range(num_twins):
        universes.append({
            "success_value": 90.0,
            "cns_wear": 0.0,
            "cognitive_focus": user_focus,
            "world_resonance": 0.5 + np.random.uniform(0.0, 0.5),
            "free_energy": 0.0,
            "qec_status": "Nominal",
            "3d_history": []
        })

    # Фиксация стартового состояния двойников (Шаг 0)
    for idx, state in enumerate(universes):
        state["3d_history"].append((state["success_value"], state["cns_wear"], state["cognitive_focus"]))
        detailed_tracks[idx].append(dict(state))

    # Сквозной цикл тактов симуляции
    for step in range(1, steps_count + 1):
        # Перехват чистого квантового потока физического вакуума
        quantum_stream, source_name = engine.get_true_quantum_stream()
        quantum_matrix.append(quantum_stream)
        source_logs.append(f"Шаг {step}: {source_name}")

        # Динамический апдейт через QEC-модуль v5.1
        if os.path.exists("modules/quantum_qec_v51.py"):
            import modules.quantum_qec_v51 as qec_v51
            importlib.reload(qec_v51)
            
            universes = qec_v51.process_multiverse_step_v51(
                universes=universes,
                step=step,
                quantum_stream=quantum_stream
            )
            
        # Синхронизация данных для графиков и SQLite-реестра логов
        for idx, state in enumerate(universes):
            if not isinstance(state, dict):
                continue
            if state.get("step_collapsed") is not None or state.get("collapsed") is True:
                state["success_value"] = 0.0
                state["cns_wear"] = 100.0
            detailed_tracks[idx].append(dict(state))

    return universes, detailed_tracks, np.array(quantum_matrix).T, source_logs
