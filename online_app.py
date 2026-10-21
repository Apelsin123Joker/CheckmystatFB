import streamlit as st
from datetime import datetime

# =====================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТАТУС САЙДБАРА
# =====================================================================
st.set_page_config(
    page_title="Darkneter Control Center",
    layout="wide",
    initial_sidebar_state="collapsed" # Скрываем стандартный сайдбар Streamlit
)

# =====================================================================
# 2. ГЛУБОКАЯ СТИЛИЗАЦИЯ (ФИРМЕННЫЙ СТИЛЬ ORBITER / DARKNETER)
# =====================================================================
st.markdown("""
    <style>
        /* Убираем стандартные отступы Streamlit для эффекта монолитного приложения */
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        div[data-testid="stSidebarCollapsedControl"] {
            display: none !important; /* Прячем кнопку раскрытия стандартного меню */
        }
        
        /* Цветовая гамма Darkneter */
        .stApp {
            background-color: #090b0e;
            color: #d1d4dc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        /* ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ (Фиксированное меню) */
        .orbiter-sidebar {
            background-color: #11141a;
            border-right: 1px solid #1c222d;
            padding: 20px 15px;
            height: 100vh;
            position: fixed;
            left: 0;
            top: 0;
            width: 240px;
            z-index: 100;
            overflow-y: auto;
        }
        .sidebar-logo {
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 25px;
        }
        .menu-section-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #4c566a;
            margin: 15px 0 5px 5px;
            font-weight: 600;
        }
        
        /* СТИЛИЗАЦИЯ ИНТЕРАКТИВНЫХ КНОПОК ПОД ДИЗАЙН ТРЕКЕРА */
        .div-btn div button {
            background-color: transparent !important;
            color: #8f9aa9 !important;
            border: none !important;
            text-align: left !important;
            padding: 6px 5px !important;
            font-size: 14px !important;
            width: 100% !important;
            line-height: 1.5 !important;
            min-height: 0px !important;
        }
        .div-btn div button:hover {
            color: #00ff88 !important;
            background-color: #162221 !important;
        }
        .div-btn-active div button {
            background-color: #162221 !important;
            color: #00ff88 !important;
            border: none !important;
            text-align: left !important;
            padding: 8px 5px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            width: 100% !important;
            border-radius: 4px !important;
        }
        
        /* ПРАВАЯ РАБОЧАЯ ЗОНА КОНТЕНТА */
        .main-content {
            margin-left: 260px; /* Отступ справа от фиксированного меню */
            padding: 25px;
        }
        .tracker-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 25px;
            border-bottom: 1px solid #1c222d;
            padding-bottom: 15px;
        }
        .tracker-title {
            font-size: 20px;
            font-weight: 600;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. УПРАВЛЕНИЕ СОСТОЯНИЕМ СТРАНИЦ (Session State)
# =====================================================================
# Программа запоминает, на какой странице находится пользователь
if "current_page" not in st.session_state:
    st.session_state.current_page = "🎯 1. Трекер"

# =====================================================================
# 4. ОТРИСОВКА ЛЕВОГО СТРУКТУРНОГО МЕНЮ
# =====================================================================
with st.container():
    st.markdown('<div class="orbiter-sidebar">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-logo">💻 Orbiter CC</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #616e88; font-size: 13px; margin-top:-20px; margin-bottom:20px;">🚨 Control Center</div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top: 1px solid #1c222d; margin-bottom: 15px;"></div>', unsafe_allow_html=True)
    
    # --- Кнопка ТРЕКЕР ---
    if st.session_state.current_page == "🎯 1. Трекер":
        st.markdown('<div class="div-btn-active">', unsafe_allow_html=True)
        st.button("🎯 1. Трекер", key="btn_tracker")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="div-btn">', unsafe_allow_html=True)
        if st.button("🎯 1. Трекер", key="btn_tracker"):
            st.session_state.current_page = "🎯 1. Трекер"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Раздел КАМПАНИИ ---
    st.markdown('<div class="menu-section-title">KAМПАНИИ</div>', unsafe_allow_html=True)
    pages_campaigns = ["🔑 Ключи", "📊 Тоталы", "🔗 Генератор ссылок"]
    for p in pages_campaigns:
        if st.session_state.current_page == p:
            st.markdown('<div class="div-btn-active">', unsafe_allow_html=True)
            st.button(p, key=f"btn_{p}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="div-btn">', unsafe_allow_html=True)
            if st.button(p, key=f"btn_{p}"):
                st.session_state.current_page = p
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Раздел КРЕАТИВЫ ---
    st.markdown('<div class="menu-section-title">КРЕАТИВЫ</div>', unsafe_allow_html=True)
    pages_creatives = ["🎬 Creative Tracker", "🎨 Creative Lab"]
    for p in pages_creatives:
        if st.session_state.current_page == p:
            st.markdown('<div class="div-btn-active">', unsafe_allow_html=True)
            st.button(p, key=f"btn_{p}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="div-btn">', unsafe_allow_html=True)
            if st.button(p, key=f"btn_{p}"):
                st.session_state.current_page = p
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Раздел META LAUNCH ---
    st.markdown('<div class="menu-section-title">META LAUNCH</div>', unsafe_allow_html=True)
    pages_meta = ["🎴 Campaign Cards", "🚀 Лаунчер", "🛡️ БМ и защита", "📂 Библиотека креативов"]
    for p in pages_meta:
        if st.session_state.current_page == p:
            st.markdown('<div class="div-btn-active">', unsafe_allow_html=True)
            st.button(p, key=f"btn_{p}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="div-btn">', unsafe_allow_html=True)
            if st.button(p, key=f"btn_{p}"):
                st.session_state.current_page = p
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Раздел УТИЛИТЫ ---
    st.markdown('<div class="menu-section-title">УТИЛИТЫ</div>', unsafe_allow_html=True)
    pages_utils = ["👥 Пользователи", "🔔 Напоминания"]
    for p in pages_utils:
        if st.session_state.current_page == p:
            st.markdown('<div class="div-btn-active">', unsafe_allow_html=True)
            st.button(p, key=f"btn_{p}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="div-btn">', unsafe_allow_html=True)
            if st.button(p, key=f"btn_{p}"):
                st.session_state.current_page = p
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
# 5. ПРАВАЯ ЧАСТЬ: ИЗМЕНЕНИЕ ЭКРАНОВ ПРИ КЛИКАХ (КОНТЕНТ)
# =====================================================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- ЭКРАН 1: ТРЕКЕР ---
if st.session_state.current_page == "🎯 1. Трекер":
    st.markdown("""
    <div class="tracker-header">
        <span class="tracker-title">🛸 Трекер</span>
        <span style="color: #8f9aa9; font-size: 14px; border-bottom: 2px solid #00ff88; padding-bottom: 5px; font-weight: 600;">Кампании</span>
        <span style="color: #4c566a; font-size: 14px; padding-bottom: 5px;">Домены</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Переносим выбор даты наверх
    col_date, col_search, _ = st.columns()
    with col_date:
        st.date_input("📅 Выберите период:", datetime.now(), label_visibility="collapsed")
    with col_search:
        st.text_input("🔍 Search campaign...", label_visibility="collapsed", placeholder="Search campaign...")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("🦴 [Блок 1 Успешно развернут] Скелет Трекера готов. На следующем шаге мы наполним его логикой загрузки файлов.")

# --- ЭКРАН 2: ЛАУНЧЕР ---
elif st.session_state.current_page == "🚀 Лаунчер":
    st.title("🚀 Автоматический Лаунчер Кампаний")
    st.write("Скелет страницы Meta Launch готов.")
    st.info("Здесь будет логика массового запуска аккаунтов Facebook.")

# --- ЭКРАН 3: ГЕНЕРАТОР ССЫЛОК ---
elif st.session_state.current_page == "🔗 Генератор ссылок":
    st.title("🔗 Конструктор потоков (TDS)")
    st.write("Скелет страницы Генератора готов.")
    st.info("Здесь мы запрограммируем создание ссылок и фильтрацию ботов.")

# --- ВСЕ ОСТАЛЬНЫЕ КНОПКИ (Универсальная заглушка) ---
else:
    st.title(f"🛠️ Раздел: {st.session_state.current_page}")

