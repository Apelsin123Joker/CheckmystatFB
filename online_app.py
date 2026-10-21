import streamlit as st
from datetime import datetime

# =====================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТАТУС САЙДБАРА
# =====================================================================
st.set_page_config(
    page_title="Darkneter Control Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# 2. ГЛУБОКАЯ СТИЛИЗАЦИЯ (ФИРМЕННЫЙ СТИЛЬ ORBITER / DARKNETER)
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
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. УПРАВЛЕНИЕ СОСТОЯНИЕМ СТРАНИЦ (Session State)
# =====================================================================
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
    
    # Кнопка ТРЕКЕР
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

    # Раздел КАМПАНИИ
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

    # Раздел КРЕАТИВЫ
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

    # Раздел META LAUNCH
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

    # Раздел УТИЛИТЫ
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

if st.session_state.current_page == "🎯 1. Трекер":
    st.markdown("""
    <div class="tracker-header">
        <span class="tracker-title">🛸 Трекер</span>
        <span style="color: #8f9aa9; font-size: 14px; border-bottom: 2px solid #00ff88; padding-bottom: 5px; font-weight: 600;">Кампании</span>
        <span style="color: #4c566a; font-size: 14px; padding-bottom: 5px;">Домены</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Поля даты и поиска наверх рабочей зоны
    col_date, col_search, _ = st.columns(3)
    with col_date:
        выбранная_дата = st.date_input("📅 Выберите период:", datetime.now(), label_visibility="collapsed").strftime("%Y-%m-%d")
    with col_search:
        st.text_input("🔍 Search campaign...", label_visibility="collapsed", placeholder="Search campaign...")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Два параллельных Drag-and-Drop бокса для импорта файлов
    st.markdown("### 📥 Импорт данных для сведения ROI")
    col_fb, col_pa = st.columns(2)

    with col_fb:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        uploaded_fb = st.file_uploader("👉 Шаг 1: Загрузить РАСХОДЫ Facebook (.xlsx)", type=["xlsx", "xls"], key="main_fb")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_pa:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        uploaded_pa = st.file_uploader("👉 Шаг 2: Загрузить ВЫРУЧКУ CRM / Партнерки (.xlsx, .csv)", type=["xlsx", "xls", "csv"], key="main_pa")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 3. Служебные переменные для матчинга (измени имена столбцов под свой Excel, если нужно)
    КОЛОНКА_ИМЯ_КАМПАНИИ_FB = "Название кампании"
    КОЛОНКА_РАСХОДЫ_FB = "Потрачено (USD)"

    # 4. Логика обработки и сведения данных при загрузке обоих отчетов
    if uploaded_fb is not None and uploaded_pa is not None:
        df_fb = pd.read_excel(uploaded_fb)
        df_pa = pd.read_csv(uploaded_pa) if uploaded_pa.name.endswith('.csv') else pd.read_excel(uploaded_pa)
            
        if КОЛОНКА_ИМЯ_КАМПАНИИ_FB in df_fb.columns:
            # Сведение расходов FB
            df_fb = df_fb[[КОЛОНКА_ИМЯ_КАМПАНИИ_FB, КОЛОНКА_РАСХОДЫ_FB]].copy()
            df_fb.columns = ["CAMPAIGN", "COST"]
            df_fb = df_fb.groupby("CAMPAIGN", as_index=False)["COST"].sum()
            
            # Автоподбор колонок в файле партнерки
            pa_name_col = "Campaign" if "Campaign" in df_pa.columns else df_pa.columns[0]
            pa_rev_col = "Revenue" if "Revenue" in df_pa.columns else df_pa.columns[1]
            
            df_pa = df_pa[[pa_name_col, pa_rev_col]].copy()
            df_pa.columns = ["CAMPAIGN", "REVENUE"]
            df_pa = df_pa.groupby("CAMPAIGN", as_index=False)["REVENUE"].sum()
            
            # Магия мэтчинга и расчета ROI / Профита
            df_final = pd.merge(df_fb, df_pa, on="CAMPAIGN", how="outer").fillna(0)
            df_final["PROFIT"] = df_final["REVENUE"] - df_final["COST"]
            df_final["ROI %"] = df_final.apply(lambda r: (r["PROFIT"] / r["COST"] * 100) if r["COST"] > 0 else 0, axis=1)
            
            # Формирование оригинальных элементов Orbiter
            df_final["STATUS PK"] = "🟢"
            df_final["ОФФЕРЫ QL"] = df_final["CAMPAIGN"].apply(lambda name: f"{str(name)[:15]}... 100%")
            
            df_final = df_final[["CAMPAIGN", "STATUS PK", "ОФФЕРЫ QL", "COST", "REVENUE", "PROFIT", "ROI %"]]
            df_final = df_final.round(2).sort_values(by="COST", ascending=False)
            
            # Строка TOTAL в самый низ таблицы
            total_cost = df_final["COST"].sum()
            total_revenue = df_final["REVENUE"].sum()
            total_profit = total_revenue - total_cost
            total_roi = (total_profit / total_cost * 100) if total_cost > 0 else 0
            
            row_total = pd.DataFrame([{
                "CAMPAIGN": f"Total ({len(df_final)} кампаний)", "STATUS PK": "📊", "ОФФЕРЫ QL": "—",
                "COST": total_cost, "REVENUE": total_revenue, "PROFIT": total_profit, "ROI %": total_roi
            }])
            df_final = pd.concat([df_final, row_total], ignore_index=True)
            
            # Рендер финальной строгой таблицы аналитики
            st.dataframe(
                df_final, use_container_width=True, hide_index=True,
                column_config={
                    "CAMPAIGN": "CAMPAIGN", "STATUS PK": "STATUS PK", "ОФФЕРЫ QL": "ОФФЕРЫ QL",
                    "COST": st.column_config.NumberColumn("COST", format="$%.2f"),
                    "REVENUE": st.column_config.NumberColumn("REVENUE", format="$%.2f"),
                    "PROFIT": st.column_config.NumberColumn("PROFIT", format="$%.2f"),
                    "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%")
                }
            )
        else:
            st.error(f"В файле FB не найден столбец '{КОЛОНКА_ИМЯ_КАМПАНИИ_FB}'")
    elif uploaded_fb is not None or uploaded_pa is not None:
        st.warning("📊 Загрузите ОБА файла одновременно, чтобы софт свел прибыль и затраты.")
    else:
        st.info("💡 Панель готова к работе. Перетащите файлы со спендом FB и ревеню партнерки в поля выше.")

elif st.session_state.current_page == "🚀 Лаунчер":
    st.title("🚀 Автоматический Лаунчер Кампаний")
    st.write("Скелет страницы Meta Launch готов.")
    st.info("Здесь будет логика массового запуска аккаунтов Facebook.")

elif st.session_state.current_page == "🔗 Генератор ссылок":
    st.title("🔗 Конструктор потоков (TDS)")
    st.write("Скелет страницы Генератора готов.")
    st.info("Здесь мы запрограммируем создание ссылок и фильтрацию ботов.")

else:
    st.title(f"🛠️ Раздел: {st.session_state.current_page}")
    st.write("Скелет страницы успешно создан.")
    st.info("Данный блок будет наполняться функционалом на следующих этапах разработки.")

st.markdown('</div>', unsafe_allow_html=True)

