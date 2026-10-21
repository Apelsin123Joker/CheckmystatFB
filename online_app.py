import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТАТУС САЙДБАРА
# =====================================================================
st.set_page_config(
    page_title="Orbiter Control Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# 2. ГЛУБОКАЯ СТИЛИЗАЦИЯ ПОД ОРИГИНАЛЬНЫЙ ТРЕКЕР
# =====================================================================
st.markdown("""
    <style>
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        div[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        .stApp {
            background-color: #090b0e;
            color: #d1d4dc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        /* Левое меню */
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
        /* Кнопки меню */
        .div-btn div button {
            background-color: transparent !important;
            color: #8f9aa9 !important;
            border: none !important;
            text-align: left !important;
            padding: 6px 5px !important;
            font-size: 14px !important;
            width: 100% !important;
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
            font-weight: 600 !important;
            border-radius: 4px !important;
        }
        /* Правая часть */
        .main-content {
            margin-left: 260px;
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
        
        /* ЖЕСТКИЙ ФИКС ДЛЯ КНОПОК ЗАГРУЗКИ: Выравниваем их в одну линию по высоте с поиском */
        div[data-testid="stColumn"] {
            display: flex;
            align-items: flex-end !important;
        }
        div[data-testid="stFileUploader"] {
            width: 100% !important;
            margin-top: 0px !important;
            padding-top: 0px !important;
        }
        div[data-testid="stFileUploaderDropzone"] {
            padding: 6px 10px !important;
            background-color: #11141a !important;
            border: 1px solid #1c222d !important;
            height: 42px !important; /* Делаем высоту один в один как у инпута поиска */
        }
        /* Прячем лишний текст внутри загрузчиков, чтобы они не раздувались */
        div[data-testid="stFileUploaderDropzone"] small {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Имена столбцов Excel для сведения
КОЛОНКА_ИМЯ_КАМПАНИИ_FB = "Название кампании"
КОЛОНКА_РАСХОДЫ_FB = "Потрачено (USD)"

# Запоминание кликов в меню
if "current_page" not in st.session_state:
    st.session_state.current_page = "🎯 1. Трекер"

# =====================================================================
# 3. ОТРИСОВКА МЕНЮ СЛЕВА
# =====================================================================
with st.container():
    st.markdown('<div class="orbiter-sidebar">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-logo">💻 Orbiter CC</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #616e88; font-size: 13px; margin-top:-20px; margin-bottom:20px;">🚨 Control Center</div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top: 1px solid #1c222d; margin-bottom: 15px;"></div>', unsafe_allow_html=True)
    
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
# 4. РАБОЧАЯ ОБЛАСТЬ СПРАВА
# =====================================================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state.current_page == "🎯 1. Трекер":
    st.markdown("""
    <div class="tracker-header">
        <span class="tracker-title">🛸 Трекер</span>
        <span style="color: #8f9aa9; font-size: 14px; border-bottom: 2px solid #00ff88; padding-bottom: 5px; font-weight: 600;">Кампании</span>
        <span style="color: #4c566a; font-size: 14px; padding-bottom: 5px;">Домены</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Идеальная верхняя линия управления: Дата, Поиск и кнопки загрузки
    col_date, col_search, col_fb, col_pa = st.columns([1, 1.5, 2, 2])
    
    with col_date:
        выбранная_дата = st.date_input("📅 Период", datetime.now(), label_visibility="collapsed").strftime("%Y-%m-%d")
    with col_search:
        st.text_input("🔍 Search...", label_visibility="collapsed", placeholder="Search campaign...")
    with col_fb:
        uploaded_fb = st.file_uploader("📥 Спенд FB (.xlsx)", type=["xlsx", "xls"], key="main_fb", label_visibility="collapsed")
    with col_pa:
        uploaded_pa = st.file_uploader("📥 Выручка ПП (.xlsx, .csv)", type=["xlsx", "xls", "csv"], key="main_pa", label_visibility="collapsed")

    st.markdown("<hr style='margin-top:10px; margin-bottom:20px;'>", unsafe_allow_html=True)

    # Логика обработки загруженных отчетов
    if uploaded_fb is not None and uploaded_pa is not None:
        try:
            # 1. Читаем данные из загруженных файлов
            df_fb = pd.read_excel(uploaded_fb)
            df_pa = pd.read_csv(uploaded_pa) if uploaded_pa.name.endswith('.csv') else pd.read_excel(uploaded_pa)
                
            # Проверяем, есть ли в файле FB нужная колонка с именами кампаний
            if КОЛОНКА_ИМЯ_КАМПАНИИ_FB in df_fb.columns:
                # Группируем и суммируем расходы по кампаниям Facebook
                df_fb = df_fb[[КОЛОНКА_ИМЯ_КАМПАНИИ_FB, КОЛОНКА_РАСХОДЫ_FB]].copy()
                df_fb.columns = ["CAMPAIGN", "COST"]
                df_fb = df_fb.groupby("CAMPAIGN", as_index=False)["COST"].sum()
                
                # Автоматически подбираем имена колонок для партнерки (поддерживает и 'Campaign' и 'Revenue')
                pa_name_col = "Campaign" if "Campaign" in df_pa.columns else df_pa.columns[0]
                pa_rev_col = "Revenue" if "Revenue" in df_pa.columns else df_pa.columns[1]
                
                # Группируем и суммируем выручку из партнерки
                df_pa = df_pa[[pa_name_col, pa_rev_col]].copy()
                df_pa.columns = ["CAMPAIGN", "REVENUE"]
                df_pa = df_pa.groupby("CAMPAIGN", as_index=False)["REVENUE"].sum()
                
                # 2. МЭТЧИНГ: Сводим расходы и доходы в одну финальную таблицу
                df_final = pd.merge(df_fb, df_pa, on="CAMPAIGN", how="outer").fillna(0)
                
                # Математические расчеты профита и окупаемости (ROI)
                df_final["PROFIT"] = df_final["REVENUE"] - df_final["COST"]
                df_final["ROI %"] = df_final.apply(lambda r: (r["PROFIT"] / r["COST"] * 100) if r["COST"] > 0 else 0, axis=1)
                
                # Добавляем оригинальные визуальные элементы Orbiter
                df_final["STATUS PK"] = "🟢"
                df_final["ОФФЕРЫ QL"] = df_final["CAMPAIGN"].apply(lambda name: f"{str(name)[:15]}... 100%")
                
                # Выстраиваем точный порядок столбцов
                df_final = df_final[["CAMPAIGN", "STATUS PK", "ОФФЕРЫ QL", "COST", "REVENUE", "PROFIT", "ROI %"]]
                df_final = df_final.round(2).sort_values(by="COST", ascending=False)
                
                # 3. Расчет финальной строки TOTAL (Итого) внизу таблицы
                total_cost = df_final["COST"].sum()
                total_revenue = df_final["REVENUE"].sum()
                total_profit = total_revenue - total_cost
                total_roi = (total_profit / total_cost * 100) if total_cost > 0 else 0
                
                row_total = pd.DataFrame([{
                    "CAMPAIGN": f"Total ({len(df_final)} РК)", 
                    "STATUS PK": "📊", 
                    "ОФФЕРЫ QL": "—",
                    "COST": total_cost, 
                    "REVENUE": total_revenue, 
                    "PROFIT": total_profit,
                    "ROI %": total_roi
                }])
                df_final = pd.concat([df_final, row_total], ignore_index=True)
                
                # 4. Рендеринг готовой таблицы результатов
                st.dataframe(
                    df_final, use_container_width=True, hide_index=True,
                    column_config={
                        "CAMPAIGN": "CAMPAIGN", 
                        "STATUS PK": "STATUS PK", 
                        "ОФФЕРЫ QL": "ОФФЕРЫ QL",
                        "COST": st.column_config.NumberColumn("COST", format="$%.2f"),
                        "REVENUE": st.column_config.NumberColumn("REVENUE", format="$%.2f"),
                        "PROFIT": st.column_config.NumberColumn("PROFIT", format="$%.2f"),
                        "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%")
                    }
                )
            else:
                st.error(f"В файле FB не найден столбец '{КОЛОНКА_ИМЯ_КАМПАНИИ_FB}'")
        except Exception as e:
            st.error(f"Ошибка парсинга: {e}")
            
    elif uploaded_fb is not None or uploaded_pa is not None:
        st.warning("📊 Загрузите ОБА файла одновременно для сведения ROI связок.")
    else:
        st.info("💡 Панель готова. Перетащите файлы расходов FB и выручки ПП в маленькие кнопки управления выше.")

elif st.session_state.current_page == "🚀 Лаунчер":
    st.title("🚀 Автоматический Лаунчер Кампаний")
    st.info("Здесь будет логика массового запуска рекламных аккаунтов Facebook.")

elif st.session_state.current_page == "🔗 Генератор ссылок":
    st.title("🔗 Конструктор потоков (TDS)")
    st.info("Здесь мы настроим генерацию ссылок с распределением трафика.")

else:
    st.title(f"🛠️ Раздел: {st.session_state.current_page}")
    st.info("Этот модуль будет наполняться функционалом на следующих этапах разработки.")

st.markdown('</div>', unsafe_allow_html=True)
