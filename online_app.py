import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================================
# КОНФИГУРАЦИЯ СТРАНИЦЫ И ОТКЛЮЧЕНИЕ ДЕФОЛТНОГО САЙДБАРА
# =====================================================================
st.set_page_config(
    page_title="Orbiter Control Center",
    layout="wide",
    initial_sidebar_state="collapsed" # Скрываем стандартное боковое меню
)

# Глубокая CSS-стилизация под интерфейс оригинального Orbiter
st.markdown("""
    <style>
        /* Полное отключение отступов Streamlit */
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        div[data-testid="stSidebarCollapsedControl"] {
            display: none !important; /* Убираем кнопку раскрытия сайдбара */
        }
        
        /* Главный контейнер приложения */
        .stApp {
            background-color: #090b0e;
            color: #d1d4dc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        /* ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ (Копия Orbiter) */
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
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .menu-section-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #4c566a;
            margin: 20px 0 10px 5px;
            font-weight: 600;
        }
        
        /* РАБОЧАЯ ОБЛАСТЬ СПРАВА */
        .main-content {
            margin-left: 260px; /* Отступ под левую панель */
            padding: 25px;
        }
        
        /* ВЕРХНЯЯ НАВИГАЦИЯ ВНУТРИ ТРЕКЕРА */
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
            margin-right: 20px;
        }
        
        /* Элементы ввода файлов */
        .upload-box {
            background-color: #11141a;
            border: 1px dashed #2d3648;
            border-radius: 6px;
            padding: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# СЛУЖЕБНЫЕ НАСТРОЙКИ ДЛЯ МАТЧИНГА ТАБЛИЦ
# =====================================================================
КОЛОНКА_ИМЯ_КАМПАНИИ_FB = "Название кампании"
КОЛОНКА_РАСХОДЫ_FB = "Потрачено (USD)"

# =====================================================================
# ЛЕВАЯ ПАНЕЛЬ: ОТОБРАЖЕНИЕ СТРУКТУРЫ МЕНЮ ORBITER
# =====================================================================
# Формируем HTML-код боковой панели с иконкой ноутбука в самом верху
st.markdown("""
<div class="orbiter-sidebar">
    <div class="sidebar-logo">💻 Orbiter CC</div>
    <div style="color: #616e88; font-size: 13px; margin-top:-20px; margin-bottom:20px;">🚨 Control Center</div>
    <div style="border-top: 1px solid #1c222d; margin-bottom: 15px;"></div>
    
    <div style="color: #00ff88; font-weight: 600; padding: 8px 5px; border-radius: 4px; background: #162221; margin-bottom: 15px; font-size: 14px;">🎯 1. Трекер</div>
    
    <div class="menu-section-title">КАМПАНИИ</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🔑 Ключи</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">📊 Тоталы</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🔗 Генератор ссылок</div>
    
    <div class="menu-section-title">КРЕАТИВЫ</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🎬 Creative Tracker</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🎨 Creative Lab</div>
    
    <div class="menu-section-title">META LAUNCH</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🎴 Campaign Cards</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🚀 Лаунчер</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🛡️ БМ и защита</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">📂 Библиотека креативов</div>
    
    <div class="menu-section-title">УТИЛИТЫ</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">👥 Пользователи</div>
    <div style="color: #8f9aa9; padding: 6px 5px; font-size: 14px; cursor: pointer;">🔔 Напоминания</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# ПРАВАЯ ЧАСТЬ: ОСНОВНАЯ РАБОЧАЯ ОБЛАСТЬ ТРЕКЕРА
# =====================================================================
# Оборачиваем всю правую часть в блок с отступом, чтобы контент не налезал на меню
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- ВЕРХНЯЯ СТРОКА НАВИГАЦИИ (Календарь и Поиск над таблицей) ---
st.markdown("""
<div class="tracker-header">
    <span class="tracker-title">🛸 Трекер</span>
    <span style="color: #8f9aa9; font-size: 14px; border-bottom: 2px solid #00ff88; padding-bottom: 5px; font-weight: 600;">Кампании</span>
    <span style="color: #4c566a; font-size: 14px; padding-bottom: 5px;">Домены</span>
</div>
""", unsafe_allow_html=True)

# Переносим выбор даты в правую рабочую зону наверх
col_date, col_search, col_spacer = st.columns([2, 3, 4])
with col_date:
    выбранная_дата = st.date_input("📅 Выберите период:", datetime.now(), label_visibility="collapsed").strftime("%Y-%m-%d")
with col_search:
    st.text_input("🔍 Search campaign...", label_visibility="collapsed", placeholder="Search campaign...")

st.markdown("<br>", unsafe_allow_html=True)

# --- ЦЕНТРАЛЬНЫЙ БЛОК ДЛЯ ЗАГРУЗКИ ФАЙЛОВ (FB COST + РЕВЕНЮ ПАРТНЕРКИ) ---
st.markdown("### 📥 Импорт данных для сведения ROI")
col_fb, col_pa = st.columns(2)

with col_fb:
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_fb = st.file_uploader("👉 Шаг 1: Загрузить РАСХОДЫ Facebook (.xlsx)", type=["xlsx", "xls"], key="main_fb")
    st.markdown('</div>', unsafe_allow_html=True)
    
with col_pa:
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_pa = st.file_uploader("👉 Шаг 2: Загрузить ВЫРУЧКУ Партнерки/CRM (.xlsx, .csv)", type=["xlsx", "xls", "csv"], key="main_pa")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- ЛОГИКА ОБРАБОТКИ И ВЫВОДА ТАБЛИЦЫ ---
if uploaded_fb is not None and uploaded_pa is not None:
    # Загружаем спенд FB
    df_fb = pd.read_excel(uploaded_fb)
    
    # Загружаем доходы партнерки
    if uploaded_pa.name.endswith('.csv'):
        df_pa = pd.read_csv(uploaded_pa)
    else:
        df_pa = pd.read_excel(uploaded_pa)
        
    # Базовый матчинг данных по именам кампаний
    if КОЛОНКА_ИМЯ_КАМПАНИИ_FB in df_fb.columns:
        df_fb = df_fb[[КОЛОНКА_ИМЯ_КАМПАНИИ_FB, КОЛОНКА_РАСХОДЫ_FB]].copy()
        df_fb.columns = ["CAMPAIGN", "COST"]
        df_fb = df_fb.groupby("CAMPAIGN", as_index=False)["COST"].sum()
        
        # Определяем имена колонок партнерки (автоматический подбор)
        pa_name_col = "Campaign" if "Campaign" in df_pa.columns else df_pa.columns[0]
        pa_rev_col = "Revenue" if "Revenue" in df_pa.columns else df_pa.columns[1]
        
        df_pa = df_pa[[pa_name_col, pa_rev_col]].copy()
        df_pa.columns = ["CAMPAIGN", "REVENUE"]
        df_pa = df_pa.groupby("CAMPAIGN", as_index=False)["REVENUE"].sum()
        
        # Полное объединение (Матчинг)
        df_final = pd.merge(df_fb, df_pa, on="CAMPAIGN", how="outer").fillna(0)
        
        # Вычисляем профит и ROI
        df_final["PROFIT"] = df_final["REVENUE"] - df_final["COST"]
        df_final["ROI %"] = df_final.apply(lambda r: (r["PROFIT"] / r["COST"] * 100) if r["COST"] > 0 else 0, axis=1)
        
        # Формируем структуру колонок один в один как в Orbiter
        df_final["STATUS PK"] = "🟢"
        # Для имитации столбца "ОФФЕРЫ QL" склеиваем имя
        df_final["ОФФЕРЫ QL"] = df_final["CAMPAIGN"].apply(lambda name: f"{name[:15]}... 100%")
        
        # Перестраиваем порядок столбцов в соответствии с эталоном Orbiter
        df_final = df_final[["CAMPAIGN", "STATUS_PK", "ОФФЕРЫ QL", "COST", "REVENUE", "PROFIT", "ROI %"]]
        df_final = df_final.round(2).sort_values(by="COST", ascending=False)
        
        # Добавляем финальную строку TOTAL внизу таблицы
        total_cost = df_final["COST"].sum()
        total_revenue = df_final["REVENUE"].sum()
        total_profit = total_revenue - total_cost
        total_roi = (total_profit / total_cost * 100) if total_cost > 0 else 0
        
        row_total = pd.DataFrame([{
            "CAMPAIGN": f"Total ({len(df_final)} кампаний)",
            "STATUS PK": "📊",
            "ОФФЕРЫ QL": "—",
            "COST": total_cost,
            "REVENUE": total_revenue,
            "PROFIT": total_profit,
            "ROI %": total_roi
        }])
        df_final = pd.concat([df_final, row_total], ignore_index=True)
        
        # Отрисовка строгой таблицы аналитики
        st.write("### 📊 Сводный отчёт за выбранный период")
        st.dataframe(
            df_final,
            use_container_width=True,
            hide_index=True,
        column_config={
    "CAMPAIGN": st.column_config.TextColumn("CAMPAIGN"),
    "STATUS PK": st.column_config.TextColumn("STATUS PK"),
    "ОФФЕРЫ QL": st.column_config.TextColumn("ОФФЕРЫ QL"),
    "COST": st.column_config.NumberColumn("COST", format="$%.2f"),
    "REVENUE": st.column_config.NumberColumn("REVENUE", format="$%.2f"),
    "PROFIT": st.column_config.NumberColumn("PROFIT", format="$%.2f"),
    "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%")
}
)
else:
st.error(f"В файле Facebook не найдена колонка расходов '{КОЛОНКА_ИМЯ_КАМПАНИИ_FB}'!")
