"""
Прототип ВКР
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""
import streamlit as st
import pandas as pd
from pathlib import Path

from src.data_loader import load_products
from src.embeddings import create_product_embeddings
from src.model import semantic_search, get_similar_products, get_recommended_accessories

st.set_page_config(page_title="ИИ Помощник по Рыбалке", page_icon="🎣", layout="wide")

st.title("🎣 Интеллектуальный помощник по подбору рыболовных товаров")
st.markdown("**Семантический поиск • Похожие товары • Корзина**")

# Корзина 
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(item):
    st.session_state.cart.append(item.copy())
    st.success(f" **{item['name']}** добавлен в корзину!")
    st.rerun()

def show_cart():
    if st.session_state.cart:
        st.sidebar.subheader("🛒 Корзина")
        total = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.sidebar.write(f"• {item['name']} — **{item['price']:.0f} ₽**")
        st.sidebar.markdown(f"**Итого: {total:.0f} ₽**")
        if st.sidebar.button("🗑 Очистить корзину"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.sidebar.info("Корзина пуста")

def format_test_info(item):
    t_min = item.get('test_min')
    t_max = item.get('test_max')
    if pd.isna(t_min) or pd.isna(t_max):
        return ""
    return f" • {t_min}–{t_max} г"

# Боковая панель
with st.sidebar:
    mode = st.radio("Выберите режим:", 
                    ["1. Загрузка данных", 
                     "2. Создание эмбеддингов", 
                     "3. Поиск товаров",
                     "4. Похожие товары"])
    show_cart()

DATA_DIR = Path("data")

# Режимы
if mode == "1. Загрузка данных":
    if st.button("Показать каталог"):
        df = load_products(DATA_DIR)
        if df is not None:
            st.success(f"Всего товаров: {len(df)}")
            st.dataframe(df[['id','name','category','price','test_min','test_max']].head(30))

elif mode == "2. Создание эмбеддингов":
    if st.button("Пересоздать эмбеддинги"):
        with st.spinner("Генерация..."):
            create_product_embeddings(DATA_DIR)
            st.success("✅ Эмбеддинги готовы!")

elif mode == "3. Поиск товаров":
    query = st.text_input("Ваш запрос:", placeholder="Спиннинг на щуку с берега тест 10-30г до 8000")
    TOP_K = 8
    st.caption(f"📊 Будет показано **{TOP_K}** самых релевантных товаров")

    if st.button("🔍 Найти") and query.strip():
        with st.spinner("Поиск..."):
            results, recognized = semantic_search(query, top_k=TOP_K, data_dir=DATA_DIR)  
            st.session_state.current_results = results
            st.session_state.recognized = recognized   

    
    if 'recognized' in st.session_state:
        rec = st.session_state.recognized
        st.markdown("### 🎯 Распознано системой")
        col1, col2 = st.columns(2)
        
        with col1:
            if rec.get('target_fish'):
                st.write(f"**🎣 Целевая рыба:** {rec['target_fish'].capitalize()}")
            if rec.get('is_bank_fishing'):
                st.write("**📍 Тип ловли:** Береговая")

        with col2:
            if rec.get('test_min') is not None or rec.get('test_max') is not None:
                tmin = rec.get('test_min')
                tmax = rec.get('test_max')
                if tmin and tmax:
                    st.write(f"**📏 Тест:** {tmin}–{tmax} г")
                elif tmin:
                    st.write(f"**📏 Тест:** от {tmin} г")
                elif tmax:
                    st.write(f"**📏 Тест:** до {tmax} г")
            
            if rec.get('min_price') is not None:
                st.write(f"**💰 Бюджет:** от {rec['min_price']} ₽")
            if rec.get('max_price') is not None:
                st.write(f"**💰 Бюджет:** до {rec['max_price']} ₽")

    # Карточки товаров
    if 'current_results' in st.session_state:
        results = st.session_state.current_results
        cols = st.columns(4)
        for i, item in enumerate(results):
            with cols[i % 4]:
                st.markdown(f"**{item['name']}**")
                st.caption(f"{item['category']}{format_test_info(item)}")
                st.write(f"**{item['price']:.0f} ₽**")
                st.caption(item['reason'])
                if st.button("🛒 В корзину", key=f"add_search_{item.get('id', i)}"):
                    add_to_cart(item)

elif mode == "4. Похожие товары":
    st.subheader("🔄 Похожие товары + комплектующие")
    df = load_products(DATA_DIR)
    if df is not None:
        selected_name = st.selectbox("Выберите основной товар:", df['name'].tolist())
        
        if st.button("Показать рекомендации"):
            with st.spinner("Формируем комплект..."):
                similar = get_similar_products(selected_name, top_k=6, data_dir=DATA_DIR)
                main_item = df[df['name'] == selected_name].iloc[0].to_dict()
                accessories_kit = get_recommended_accessories(main_item, data_dir=DATA_DIR)
                
                st.session_state.current_similar = similar
                st.session_state.current_accessories_kit = accessories_kit
                st.session_state.selected_main = main_item

        if 'current_accessories_kit' in st.session_state:
            main = st.session_state.selected_main
            st.markdown(f"### Основной товар: **{main['name']}**")

            col1, col2 = st.columns(2)

            # Похожие товары
            with col1:
                st.subheader("🔄 Похожие товары")
                cols = st.columns(3)
                for i, item in enumerate(st.session_state.current_similar):
                    with cols[i % 3]:
                        st.markdown(f"**{item['name']}**")
                        st.caption(f"{item['category']}{format_test_info(item)}")
                        st.write(f"**{item['price']:.0f} ₽**")
                        if st.button("🛒 В корзину", key=f"sim_{i}"):
                            add_to_cart(item)

            # Необходимые аксессуары через уникальные ключи
            with col2:
                st.subheader("🛠 Необходимые аксессуары")
                for title, items in st.session_state.current_accessories_kit.items():
                    if isinstance(items, dict):
                        items = [items]
                    st.markdown(f"**{title}**")
                    for idx, item in enumerate(items):
                        st.write(f"• **{item['name']}** — {item['price']:.0f} ₽")
                        # уникальный ключ
                        safe_key = f"acc_{title[:15]}_{idx}_{hash(item.get('name', '')) % 1000000}"
                        if st.button("🛒 В корзину", key=safe_key):
                            add_to_cart(item)
                    st.divider()

st.caption("Прототип ВКР • Интеллектуальный помощник по рыбалке")