import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =====================================================================
# НАСТРОЙКИ СТИЛЯ И ИНТЕРФЕЙСА В СТИЛЕ ORBITER
# =====================================================================
st.set_page_config(
    page_title="Orbiter Control Center - Трекер",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Внедряем CSS-стили для полной имитации интерфейса Orbiter (темный фон, шрифты, границы)
st.markdown("""
    <style>
        /* Общий фон страницы и текст */
        .stApp {
            background-color: #0b0c10;
            color: #c5c6c7;
        }
        /* Боковое меню */
        section[data-testid="stSidebar"] {
            background-color: #1f2833;
            border-right: 1px solid #45a29e;
        }
        /* Стилизация заголовков */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Фирменная разделительная линия */
        hr {
            border-color: #333b4d !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# НАСТРОЙКИ ДАННЫХ (Подставьте ваши столбцы из Excel FB)
# =====================================================================
КОЛОНКА_ИМЯ_КАМПАНИИ = "Название кампании"  # Столбец из FB (например, d8x_BK_FB_LSA...)
КОЛОНКА_РАСХОДЫ = "Потрачено (USD)"       # Столбец из FB с расходами (Cost)

# =====================================================================
# ФУНКЦИЯ ДЛЯ ЗАПРОСА В API ORBITER
# =====================================================================
def получить_данные_трекера(target_date):
    """Имитация запроса к API Orbiter для получения офферов и покупок"""
    # В будущем здесь будет реальный requests.post к вашему бэкенду
    # Сейчас возвращаем демо-данные, отформатированные точно как на скрине
    demo_data = [
        {"Имя_Кампании": "c5p_BK_AAE_TR_tr_AG14_s5_rk1_16.10_s6", "STATUS_PK": "🟢", "OFFERS_QL": "c5p_BK_AAE_TR_tr_AG14... 100% (11/0)", "PURCHASES": 0},
        {"Имя_Кампании": "c5p_BK_BKVD_PL_pl_AG14_ql1_rk1_05.10_s1", "STATUS_PK": "🟢", "OFFERS_QL": "c5p_BK_BKVD_PL_pl_AG14... 100% (15/4)", "PURCHASES": 1},
        {"Имя_Кампании": "c5p_BK_AAE_TR_tr_AG14_s5_rk2_16.10_s7", "STATUS_PK": "🟢", "OFFERS_QL": "c5p_BK_AAE_TR_tr_AG14... 100% (7/0)", "PURCHASES": 0},
        {"Имя_Кампании": "d8x_BK_FB_LSA_US_es_s7_AG14_rk1_scr1", "STATUS_PK": "🟢", "OFFERS_QL": "d8x_BK_FB_LSA_US_es_s7... 100% (6/0)", "PURCHASES": 0},
    ]
    return pd.DataFrame(demo_data)

# =====================================================================
# ЭКРАН ПАНЕЛИ УПРАВЛЕНИЯ
# =====================================================================

# Меню управления слева
st.sidebar.title("🛸 Orbiter CC")
st.sidebar.write("### Панель управления")
выбранная_дата = st.sidebar.date_input("📅 Выберите дату", datetime.now()).strftime("%Y-%m-%d")
uploaded_file = st.sidebar.file_uploader("📥 Загрузить спенд FB (.xlsx)", type=["xlsx", "xls"])

# Главное окно трекера
st.title("🛸 Трекер")
st.write(f"### Аналитика за неделю/день — `{выбранная_дата}`")
st.write("---")

if uploaded_file is not None:
    # Загружаем спенд из файла
    df_fb = pd.read_excel(uploaded_file)
    
    if КОЛОНКА_ИМЯ_КАМПАНИИ in df_fb.columns and КОЛОНКА_РАСХОДЫ in df_fb.columns:
        # Форматируем траты
        df_fb = df_fb[[КОЛОНКА_ИМЯ_КАМПАНИИ, КОЛОНКА_РАСХОДЫ]].copy()
        df_fb.columns = ["CAMPAIGN", "COST"]
        df_fb = df_fb.groupby("CAMPAIGN", as_index=False)["COST"].sum()
        
        # Запрашиваем данные трекера (статусы, офферы, покупки)
        df_tracker = получить_данные_трекера(выбранная_дата)
        
        # Склеиваем таблицы по названию кампании
        # Имена колонок приведены в точное соответствие с вашим интерфейсом Orbiter
        df_final = pd.merge(df_fb, df_tracker, left_on="CAMPAIGN", right_on="Имя_Кампании", how="outer")
        
        # Если кампании нет в выгрузках, заполняем пропуски дефолтными значениями
        df_final["STATUS_PK"] = df_final["STATUS_PK"].fillna("⚪")
        df_final["OFFERS_QL"] = df_final["OFFERS_QL"].fillna("Нет данных")
        df_final["COST"] = df_final["COST"].fillna(0.0)
        df_final["PURCHASES"] = df_final["PURCHASES"].fillna(0).astype(int)
        
        # Формируем точный порядок колонок, как на скриншоте Orbiter
        df_final = df_final[["CAMPAIGN", "STATUS_PK", "OFFERS_QL", "COST", "PURCHASES"]]
        
        # Сортируем по расходам (от больших к меньшим), как принято в арбитражных таблицах
        df_final = df_final.sort_values(by="COST", ascending=False)
        
        # Считаем строку Total (Итого) в самом низу
        total_cost = df_final["COST"].sum()
        total_purchases = df_final["PURCHASES"].sum()
        
        row_total = pd.DataFrame([{
            "CAMPAIGN": f"Total ({len(df_final)} РК)",
            "STATUS_PK": "📊",
            "OFFERS_QL": "—",
            "COST": total_cost,
            "PURCHASES": total_purchases
        }])
        
        df_final = pd.concat([df_final, row_total], ignore_index=True)
        
        # Вывод таблицы в оригинальном строгом стиле
        st.dataframe(
            df_final,
            use_container_width=True,
            column_config={
                "CAMPAIGN": st.column_config.TextColumn("CAMPAIGN"),
                "STATUS_PK": st.column_config.TextColumn("STATUS PK"),
                "OFFERS_QL": st.column_config.TextColumn("ОФФЕРЫ QL"),
                "COST": st.column_config.NumberColumn("COST \(", format="\)%.2f"),
                "PURCHASES": st.column_config.NumberColumn("PURCHASES 🛒")
            },
            hide_index=True
        )
        
    else:
        st.error(f"Колонки файла не совпадают! Проверьте, есть ли '{КОЛОНКА_ИМЯ_КАМПАНИИ}' и '{КОЛОНКА_РАСХОДЫ}'")
else:
    st.info("Пожалуйста, загрузите `.xlsx` отчет с расходами Facebook в левой панели для отображения таблицы кампаний.")

