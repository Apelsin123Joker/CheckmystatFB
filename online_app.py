import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =====================================================================
# НАСТРОЙКИ ПОДКЛЮЧЕНИЯ
# =====================================================================
# Замените на реальный API URL и Ключ вашей платформы Orbiter
ORBITER_API_URL = "https://your-orbiter-domain.com" 
ORBITER_API_KEY = "ВАШ_ТОКЕН_ИЗ_ORBITER"

# Названия колонок в вашем Excel-файле из Facebook
КОЛОНКА_ИМЯ_КАМПАНИИ = "Название кампании"
КОЛОНКА_РАСХОДЫ = "Потрачено (RUB)"

# =====================================================================
# ФУНКЦИЯ ЗАПРОСА К API КОМПАНИИ (ORBITER)
# =====================================================================
def fetch_orbiter_revenue(target_date):
    """Стучится в API Orbiter и забирает выручку по кампаниям за дату"""
    headers = {
        "Authorization": f"Bearer {ORBITER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Формируем запрос под требования API вашей компании
    payload = {
        "date": target_date,
        "group_by": "campaign_name",
        "metrics": ["revenue"]
    }
    
    try:
        response = requests.post(ORBITER_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Допустим, API возвращает список: [{"campaign_name": "РК_1", "revenue": 500}]
            rows = data.get("data", [])
            return pd.DataFrame([{"Имя_Кампании": r.get("campaign_name"), "Доход": float(r.get("revenue", 0))} for r in rows])
    except Exception as e:
        st.sidebar.error(f"Ошибка API Orbiter: {e}")
        
    return pd.DataFrame(columns=["Имя_Кампании", "Доход"])

# =====================================================================
# ИНТЕРФЕЙС И ВНЕШНИЙ ВИД (КРАСИВАЯ ПАНЕЛЬ)
# =====================================================================
st.set_page_config(page_title="Orbiter Stats Matcher", layout="wide", initial_sidebar_state="expanded")

# --- БОКОВОЕ МЕНЮ (Кастомизация управления) ---
st.sidebar.image("https://icons8.com", width=60)
st.sidebar.title("Orbiter Интегратор")
st.sidebar.write("---")

выбранная_дата = st.sidebar.date_input("📅 1. Выберите дату отчета:", datetime.now()).strftime("%Y-%m-%d")
uploaded_file = st.sidebar.file_uploader("📂 2. Загрузите Excel Facebook (Спенд)", type=["xlsx", "xls"])
st.sidebar.write("---")
st.sidebar.info("Софт автоматически склеит расход из файла с доходами из API Orbiter по совпадению имен РК.")

# --- ГЛАВНЫЙ ЭКРАН ---
if uploaded_file is not None:
    # Чтение данных FB
    таблица_фб = pd.read_excel(uploaded_file)
    
    if КОЛОНКА_ИМЯ_КАМПАНИИ in таблица_фб.columns and КОЛОНКА_РАСХОДЫ in таблица_фб.columns:
        
        # Подготовка расходов
        таблица_фб = таблица_фб[[КОЛОНКА_ИМЯ_КАМПАНИИ, КОЛОНКА_РАСХОДЫ]].copy()
        таблица_фб.columns = ["Имя_Кампании", "Расход"]
        таблица_фб = таблица_фб.groupby("Имя_Кампании", as_index=False)["Расход"].sum().fillna(0)
        
        # Получение доходов из Orbiter API
        with st.spinner('⏳ Подтягиваем выручку из API Orbiter...'):
            таблица_трекера = fetch_orbiter_revenue(выбранная_дата)
            
        # Объединение
        итоговая_таблица = pd.merge(таблица_фб, таблица_трекера, on="Имя_Кампании", how="outer").fillna(0)
        итоговая_таблица["Прибыль"] = итоговая_таблица["Доход"] - итоговая_таблица["Расход"]
        итоговая_таблица["ROI %"] = итоговая_таблица.apply(lambda r: (r["Прибыль"] / r["Расход"] * 100) if r["Расход"] > 0 else 0, axis=1)
        итоговая_таблица = итоговая_таблица.round(2).sort_values(by="Прибыль", ascending=False)
        
        # ВЫВОД КРАСИВЫХ ВИДЖЕТОВ (KPI БЛОКИ)
        total_cost = итоговая_таблица["Расход"].sum()
        total_revenue = итоговая_таблица["Доход"].sum()
        total_profit = total_revenue - total_cost
        total_roi = (total_profit / total_cost * 100) if total_cost > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Всего Расход (FB)", f"{total_cost:,.2f} ₽")
        col2.metric("📈 Всего Выручка (Orbiter)", f"{total_revenue:,.2f} ₽")
        
        # Подсвечиваем прибыль зеленым или красным
        if total_profit >= 0:
            col3.metric("✅ Чистая Прибыль", f"{total_profit:,.2f} ₽", delta=f"+{total_roi:.2f}% ROI")
        else:
            col4.metric("🚨 Чистый Убыток", f"{total_profit:,.2f} ₽", delta=f"{total_roi:.2f}% ROI", delta_color="inverse")
            
        st.write("---")
        
        # ИНТЕРАКТИВНАЯ ТАБЛИЦА С СОРТИРОВКОЙ И ФИЛЬТРАМИ
        st.subheader("📋 Сводная аналитика по рекламным кампаниям")
        
        # Стилизуем таблицу, чтобы подсветить прибыльные кампании
        st.dataframe(
            итоговая_таблица, 
            use_container_width=True,
            column_config={
                "Расход": st.column_config.NumberColumn("Траты FB", format="%.2f ₽"),
                "Доход": st.column_config.NumberColumn("Выручка Orbiter", format="%.2f ₽"),
                "Прибыль": st.column_config.NumberColumn("Профит", format="%.2f ₽"),
                "ROI %": st.column_config.ProgressColumn("Окупаемость (ROI)", min_value=-100, max_value=200, format="%d%%")
            }
        )
        
    else:
        st.error(f"Ошибка структуры файла: убедитесь, что в Excel есть столбцы '{КОЛОНКА_ИМЯ_КАМПАНИИ}' и '{КОЛОНКА_РАСХОДЫ}'")
else:
    # Заглушка, если файл еще не перетащили
    st.info("👋 Добро пожаловать! Пожалуйста, выберите дату отчета и загрузите файл со спендом в левой панели меню.")
