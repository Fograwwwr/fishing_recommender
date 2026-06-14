"""
Прототип ВКР — интернет-магазин рыболовных товаров
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""
import pandas as pd
import streamlit as st
from pathlib import Path

from src.data_loader import load_products
from src.ui.catalog import (
    CATEGORY_GROUPS,
    DEFAULT_PER_PAGE,
    filter_catalog,
    format_test_info,
    get_categories_for_group,
    get_image_path,
    load_catalog,
    paginate_dataframe,
    row_to_cart_item,
    
)
from src.ui.components import (
    inject_styles,
    navigate,
    render_cart_contents,
    render_footer,
    render_header,
    render_hero,
    render_pagination_controls,
    render_product_detail,
    render_product_grid,
    render_recognized_block,
)

st.set_page_config(
    page_title="FishStore — товары для рыбалки",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = Path("data")

if "cart" not in st.session_state:
    st.session_state.cart = []
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_product_id" not in st.session_state:
    st.session_state.selected_product_id = None
if "catalog_group" not in st.session_state:
    st.session_state.catalog_group = "Все"
if "catalog_category" not in st.session_state:
    st.session_state.catalog_category = "Все"
if "catalog_page" not in st.session_state:
    st.session_state.catalog_page = 1
if "catalog_per_page" not in st.session_state:
    st.session_state.catalog_per_page = DEFAULT_PER_PAGE
if "catalog_filter_key" not in st.session_state:
    st.session_state.catalog_filter_key = ""

inject_styles()
render_header()

page = st.session_state.page

# Главная
if page == "home":
    render_hero()

    st.markdown("---")
    st.markdown("### Умный поиск с ИИ")
    st.caption("Опишите задачу своими словами — система подберёт товары по рыбе, тесту и бюджету.")
    if st.button("Перейти к умному поиску", key="home_search"):
        navigate("search")

# Каталог 
elif page == "catalog":
    st.markdown('<div class="section-title">Каталог товаров</div>', unsafe_allow_html=True)

    df = load_catalog(DATA_DIR)
    if df.empty:
        st.error("Каталог пуст. Проверьте файл data/products.csv")
    else:
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            group = st.selectbox(
                "Группа",
                ["Все"] + list(CATEGORY_GROUPS.keys()),
                index=(["Все"] + list(CATEGORY_GROUPS.keys())).index(st.session_state.catalog_group)
                if st.session_state.catalog_group in ["Все"] + list(CATEGORY_GROUPS.keys()) else 0,
                key="sel_group",
            )
            st.session_state.catalog_group = group
        with f2:
            categories = ["Все"] + get_categories_for_group(df, group)
            cat_index = categories.index(st.session_state.catalog_category) if st.session_state.catalog_category in categories else 0
            category = st.selectbox("Категория", categories, index=cat_index, key="sel_category")
            st.session_state.catalog_category = category
        with f3:
            text_filter = st.text_input("Быстрый поиск по названию", key="catalog_text_filter")

        filtered = filter_catalog(df, group=group, category=category, search_text=text_filter or None)
        per_page = st.session_state.catalog_per_page

        filter_key = f"{group}|{category}|{text_filter}|{per_page}"
        if st.session_state.catalog_filter_key != filter_key:
            st.session_state.catalog_page = 1
            st.session_state.catalog_filter_key = filter_key

        page_df, total_pages, total_items = paginate_dataframe(
            filtered,
            st.session_state.catalog_page,
            per_page,
        )
        if st.session_state.catalog_page > total_pages:
            st.session_state.catalog_page = total_pages

        st.caption(f"Найдено товаров: **{total_items}**")

        render_pagination_controls(
            st.session_state.catalog_page,
            total_pages,
            total_items,
            per_page,
            key_prefix="catalog_top",
        )

        render_product_grid(page_df, key_prefix=f"cat_p{st.session_state.catalog_page}")

        if total_pages > 1:
            st.markdown("---")
            render_pagination_controls(
                st.session_state.catalog_page,
                total_pages,
                total_items,
                per_page,
                key_prefix="catalog_bottom",
                show_per_page=False,
            )

# Карточка товара 
elif page == "product":
    df = load_catalog(DATA_DIR)
    pid = st.session_state.selected_product_id

    if pid is None or df.empty or pid not in df["id"].values:
        st.warning("Товар не выбран.")
        if st.button("Вернуться в каталог"):
            navigate("catalog")
    else:
        item = df[df["id"] == pid].iloc[0]
        image_path = get_image_path(item["category"])

        if st.button("← Назад в каталог"):
            navigate("catalog")

        render_product_detail(item, image_path if image_path.exists() else None)

        if st.button("Купить", type="primary", key="product_buy"):
            st.session_state.cart.append(row_to_cart_item(item))
            st.toast(f"{item['name']} добавлен в корзину")
            st.rerun()

        st.markdown("---")
        from src.model import get_similar_products, get_recommended_accessories

        with st.spinner("Формируем рекомендации..."):
            similar = get_similar_products(item["name"], top_k=6, data_dir=DATA_DIR)
            accessories_kit = get_recommended_accessories(item.to_dict(), data_dir=DATA_DIR)

        col_sim, col_acc = st.columns(2)
        with col_sim:
            st.subheader("Похожие товары")
            if similar:
                for i, sim in enumerate(similar):
                    st.markdown(f"**{sim['name']}** — {sim['price']:.0f} ₽")
                    st.caption(f"{sim['category']} · {sim.get('reason', '')}")
                    if st.button("В корзину", key=f"sim_buy_{i}"):
                        st.session_state.cart.append(sim)
                        st.toast("Добавлено в корзину")
                        st.rerun()
            else:
                st.caption("Похожие товары не найдены.")

        with col_acc:
            st.subheader("Необходимые аксессуары")
            if accessories_kit:
                for title, items in accessories_kit.items():
                    if isinstance(items, dict):
                        items = [items]
                    st.markdown(f"**{title}**")
                    for idx, acc in enumerate(items):
                        st.write(f"• {acc['name']} — {acc['price']:.0f} ₽")
                        if st.button("В корзину", key=f"acc_{title[:10]}_{idx}"):
                            st.session_state.cart.append({
                                "id": acc.get("id"),
                                "name": acc["name"],
                                "price": float(acc["price"]),
                                "category": acc.get("category", ""),
                            })
                            st.toast("Добавлено в корзину")
                            st.rerun()
            else:
                st.caption("Аксессуары не подобраны.")

# Умный поиск 
elif page == "search":
    st.markdown('<div class="section-title">Умный поиск</div>', unsafe_allow_html=True)
    st.caption("Опишите запрос своими словами — ИИ распознает рыбу, тест, бюджет и подберёт товары.")

    query = st.text_input(
        "Ваш запрос",
        placeholder="Спиннинг на щуку с берега тест 10-30г до 8000",
        key="search_query",
    )
    top_k = st.slider("Количество результатов", 4, 12, 8)

    if st.button("Найти", type="primary", key="search_btn") and query.strip():
        from src.model import semantic_search

        with st.spinner("Поиск..."):
            results, recognized = semantic_search(query, top_k=top_k, data_dir=DATA_DIR)
            st.session_state.search_results = results
            st.session_state.search_recognized = recognized

    if "search_recognized" in st.session_state:
        render_recognized_block(st.session_state.search_recognized)

    if "search_results" in st.session_state and st.session_state.search_results:
        st.markdown("### Результаты поиска")
        for i, item in enumerate(st.session_state.search_results):
            cols = st.columns([3, 1, 1, 1])
            with cols[0]:
                st.markdown(f"**{item['name']}**")
                st.caption(f"{item['category']}{' · ' + format_test_info(item) if format_test_info(item) else ''}")
                st.caption(item.get("reason", ""))
            with cols[1]:
                st.markdown(f"**{item['price']:.0f} ₽**")
            with cols[2]:
                if st.button("Купить", key=f"search_buy_{i}"):
                    st.session_state.cart.append(item)
                    st.toast("Добавлено в корзину")
                    st.rerun()
            with cols[3]:
                df = load_catalog(DATA_DIR)
                match = df[df["name"] == item["name"]]
                if not match.empty:
                    if st.button("Подробнее", key=f"search_view_{i}"):
                        navigate("product", selected_product_id=int(match.iloc[0]["id"]))

# Корзина 
elif page == "cart":
    st.markdown('<div class="section-title">Корзина</div>', unsafe_allow_html=True)

    cart = st.session_state.cart
    if not cart:
        st.info("Корзина пуста. Перейдите в каталог или воспользуйтесь умным поиском.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("В каталог", type="primary"):
                navigate("catalog")
        with c2:
            if st.button("Умный поиск"):
                navigate("search")
    else:
        render_cart_contents(cart)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Оформить заказ", type="primary"):
                st.success("Заказ оформлен! (демо-режим прототипа)")
        with c2:
            if st.button("Продолжить покупки"):
                navigate("catalog")
        with c3:
            if st.button("Очистить корзину"):
                st.session_state.cart = []
                st.rerun()

# Админ
elif page == "admin":
    st.markdown('<div class="section-title">Администрирование</div>', unsafe_allow_html=True)
    st.caption("Служебные функции для демонстрации и подготовки данных.")

    tab1, tab2 = st.tabs(["Каталог данных", "Эмбеддинги"])

    with tab1:
        if st.button("Показать каталог"):
            df = load_products(DATA_DIR)
            if df is not None:
                st.success(f"Всего товаров: {len(df)}")
                st.dataframe(df[["id", "name", "category", "price", "test_min", "test_max"]].head(50))

    with tab2:
        st.warning("Пересоздание эмбеддингов может занять несколько минут.")
        if st.button("Пересоздать эмбеддинги"):
            from src.embeddings import create_product_embeddings

            with st.spinner("Генерация..."):
                create_product_embeddings(DATA_DIR)
                st.success("Эмбеддинги готовы!")

    if st.button("← На главную"):
        navigate("home")

render_footer()