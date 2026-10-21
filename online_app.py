import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================================
# НАСТРОЙКИ СТИЛЯ "DARKNETER / МИНИМАЛИЗМ"
# =====================================================================
st.set_page_config(
    page_title="Darkneter Control Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Профессиональный минималистичный темный стиль без лишних рамок
st.markdown("""
    <style>
        .stApp {
            background-color: #0d0f12;
            color: #9cd1bb;
        }
        section[data-testid="stSidebar"] {
            background-color: #13171c;
            border-right: 1px solid #1f262e;
        }
        /* Кастомизация кнопок меню, чтобы они выглядели строго */
        .stButton>button {
            width: 100%;
            background-color: #1c232b;
            color: #ffffff;
            border: 1px solid #2d3846;
            text-align: left;
            padding: 10px;
            border-radius: 4px;
        }
        .stButton>button:hover {
            border-color: #00ff88;
            color: #00ff88;
        }
        h1, h2, h3 {
            font-family: 'Courier New', monospace;
            color: #ffffff !important;
        }
        hr {
            border-color: #1f262e !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# НАСТРОЙКИ НАЗВАНИЙ СТОЛБЦОВ ДЛЯ МАТЧИНГА
# =====================================================================
КОЛОНКА_ИМЯ_КАМПАНИИ = "Название кампании"
КОЛОНКА_РАСХОДЫ = "Потрачено (USD)"

# =====================================================================
# ЛЕВАЯ ПАНЕЛЬ: МЕНЮ И ПОЛНЫЙ ЦИКЛ ЗАПУСКА
# =====================================================================
# Вставляем иконку ноутбука (💻) в левый верхний угол
st.sidebar.markdown("## 💻 **DARKNETER CC**")
st.sidebar.markdown("<small style='color:#566275;'>v2.0 // Полный цикл</small>", unsafe_allow_html=True)
st.sidebar.write("---")

# Создаем переключатель разделов приложения
st.sidebar.write("### 🧭 Навигация")
раздел = st.sidebar.radio(
    label="Выберите инструмент:",
    options=[
        "🎯 1. Трекер и Аналитика",
        "📦 2. Офферы",
        "🔗 3. Создание ссылок (TDS)",
        "🎨 4. Создание креативов",
        "🚀 5. Полный цикл запуска"
    ],
    label_visibility="collapsed"
)

st.sidebar.write("---")
# Вынесли выбор даты в боковое меню под навигацию
выбранная_дата = st.sidebar.date_input("📅 Дата анализа:", datetime.now()).strftime("%Y-%m-%d")

# =====================================================================
# ПРАВАЯ ПАНЕЛЬ: ЛОГИКА ОТОБРАЖЕНИЯ РАЗДЕЛОВ
# =====================================================================

# --- РАЗДЕЛ 1: ТРЕКЕР И АНАЛИТИКА ---
if раздел == "🎯 1. Трекер и Аналитика":
    st.title("🎯 Трекер и Сведение Статистики")
    st.write(f"Сведение данных за: `{выбранная_дата}`")
    st.write("---")
    
    # Блок одновременной подгрузки данных (FB + Партнерка)
    st.subheader("📥 Входные данные для анализа")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📘 Расходы (Facebook)")
        uploaded_fb = st.file_uploader("Перетащите Excel со спендом FB", type=["xlsx", "xls"], key="fb_upload")
        
    with col_right:
        st.markdown("### 📗 Доходы (Партнерка / CRM)")
        uploaded_pa = st.file_uploader("Перетащите Excel/CSV из партнерки", type=["xlsx", "xls", "csv"], key="pa_upload")

    # Логика обработки, когда загружены ОБА файла
    if uploaded_fb is not None and uploaded_pa is not None:
        st.success("⚡ Оба файла успешно загружены! Начинаю сопоставление...")
        
        # 1. Читаем расходы FB
        df_fb = pd.read_excel(uploaded_fb)
        
        # 2. Читаем доходы партнерки
        if uploaded_pa.name.endswith('.csv'):
            df_pa = pd.read_csv(uploaded_pa)
        else:
            df_pa = pd.read_excel(uploaded_pa)
            
        # Проверка структуры файлов
        if КОЛОНКА_ИМЯ_КАМПАНИИ in df_fb.columns:
            # Обработка FB
            df_fb = df_fb[[КОЛОНКА_ИМЯ_КАМПАНИИ, КОЛОНКА_РАСХОДЫ]].copy()
            df_fb.columns = ["CAMPAIGN", "COST"]
            df_fb = df_fb.groupby("CAMPAIGN", as_index=False)["COST"].sum()
            
            # Предположим, в выгрузке партнерки колонки называются "Campaign" и "Revenue"
            # Вы можете изменить названия ниже под ваш файл партнерки
            col_pa_name = "Campaign" if "Campaign" in df_pa.columns else df_pa.columns[0]
            col_pa_rev = "Revenue" if "Revenue" in df_pa.columns else df_pa.columns[1]
            
            df_pa = df_pa[[col_pa_name, col_pa_rev]].copy()
            df_pa.columns = ["CAMPAIGN", "REVENUE"]
            df_pa = df_pa.groupby("CAMPAIGN", as_index=False)["REVENUE"].sum()
            
            # МАТЧИНГ (Сведение данных)
            df_final = pd.merge(df_fb, df_pa, on="CAMPAIGN", how="outer").fillna(0)
            
            # Вычисления математики
            df_final["PROFIT"] = df_final["REVENUE"] - df_final["COST"]
            df_final["ROI %"] = df_final.apply(lambda r: (r["PROFIT"] / r["COST"] * 100) if r["COST"] > 0 else 0, axis=1)
            
            df_final = df_final.round(2).sort_values(by="PROFIT", ascending=False)
            
            # Вывод итоговой таблицы
            st.write("### 📊 Итоговый Сводный Отчет")
            st.dataframe(
                df_final, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "CAMPAIGN": "Название Кампании",
                    "COST": st.column_config.NumberColumn("Расход FB (\$)", format="\$%.2f"),
                    "REVENUE": st.column_config.NumberColumn("Доход ПП (\$)", format="\$%.2f"),
                    "PROFIT": st.column_config.NumberColumn("Профит (\$)", format="\$%.2f"),
                    "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%")
                }
            )
        else:
            st.error("В файле Facebook не найден столбец 'Название кампании'!")
            
    elif uploaded_fb is not None or uploaded_pa is not None:
        st.warning("⚠️ Для расчета общего ROI необходимо загрузить оба файла одновременно (и спенд, и ревеню).")
    else:
        st.info("💡 Загрузите отчеты в панели выше, чтобы софт автоматически рассчитал профит по каждой связке.")

# --- ОСТАЛЬНЫЕ ВТАКЛАДКИ ДЛЯ ПОЛНОГО ЦИКЛА ЗАПУСКА (Заглушки для будущего кода) ---
elif раздел == "📦 2. Офферы":
    st.title("📦 Менеджер Офферов")
    st.write("Здесь будет список подключенных офферов, гео, ставок и рекламодателей.")
    st.text_input("Поиск активного оффера:")
    
elif раздел == "🔗 3. Создание ссылок (TDS)":
    st.title("🔗 Конструктор потоков и Клоакинг")
    st.write("Генератор безопасных ссылок распределения трафика (TDS).")
    st.text_input("Введите целевую ссылку (Safe Page):")
    st.text_input("Введите black page (Оффер):")
    st.button("Сгенерировать поток")

elif раздел == "🎨 4. Создание креативов":
    st.title("🎨 Библиотека и уникализатор креативов")
    st.write("Инструменты пакетного изменения метаданных картинок и видео перед заливом в FB.")
    st.file_uploader("Загрузите креатив для очистки метаданных", type=["jpg", "png", "mp4"])

elif раздел == "🚀 5. Полный цикл запуска":
    st.title("🚀 Автоматизация запуска (Full Cycle)")
    st.write("Сводный чеклист и автоматизация отправки кампаний в рекламные кабинеты.")
    st.checkbox("Шаг 1: Проверка прокси и аккаунтов")
    st.checkbox("Шаг 2: Привязка платежек")
    st.checkbox("Шаг 3: Прогрев и запуск пролей")
