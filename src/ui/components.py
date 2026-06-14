"""
UI-компоненты магазина для Streamlit.
"""

import base64
import html
from pathlib import Path

import pandas as pd
import streamlit as st

from src.ui.catalog import (
    format_test_info,
    get_image_path,
    truncate_text,
)

ROOT = Path(__file__).resolve().parents[2]
STYLES_PATH = ROOT / "assets" / "style.css"
HERO_IMAGE_PATH = ROOT / "assets" / "images" / "hero-fishing.jpg"


def inject_styles():
    if STYLES_PATH.exists():
        css = STYLES_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _image_to_data_uri(image_path: Path) -> str:
    suffix = image_path.suffix.lower()
    mime = "image/svg+xml" if suffix == ".svg" else "image/png"
    data = base64.b64encode(image_path.read_bytes()).decode()
    return f"data:{mime};base64,{data}"


def navigate(page: str, **extra):
    st.session_state.page = page
    for key, value in extra.items():
        st.session_state[key] = value
    st.rerun()


def render_header():
    cart_count = len(st.session_state.get("cart", []))
    cart_label = f"Корзина ({cart_count})" if cart_count else "Корзина"

    st.markdown(
        """
        <div class="store-header">
            <div class="store-header-top">
                <div>
                    <div class="store-logo">🎣 FishStore</div>
                    <div class="store-tagline">Интернет-магазин товаров для рыбалки</div>
                </div>
                <div class="store-phone">
                    <a href="tel:89999999999">8 (999) 999-99-99</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(5)
    nav_items = [
        ("Главная", "home"),
        ("Каталог", "catalog"),
        ("Умный поиск", "search"),
        (cart_label, "cart"),
    ]
    for i, (label, page) in enumerate(nav_items):
        with cols[i]:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                navigate(page)

    with cols[4]:
        if st.button("⚙ Админ", key="nav_admin", use_container_width=True):
            navigate("admin")


def render_footer():
    st.markdown(
        """
        <div class="store-footer">
            <h4>Как нас найти</h4>
            <p>г. Москва<br>
            E-mail: fishing@mail.ru<br>
            Телефон: 8 (999) 999-99-99 — отдел продаж</p>
            <p style="margin-top:1rem;opacity:0.8;">
            Интернет-магазин товаров для рыбалки · Прототип ВКР
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    hero_img = ""
    if HERO_IMAGE_PATH.exists():
        hero_img = _image_to_data_uri(HERO_IMAGE_PATH)

    st.markdown(
        f"""
        <div class="hero-section">
            <div class="hero-layout">
                <div class="hero-content">
                    <div class="hero-title">Интернет-магазин товаров для рыбалки</div>
                    <div class="hero-subtitle">
                        Высокое качество. Быстрая доставка.
                    </div>
                    <div class="hero-features">
                        <span class="hero-feature">Неповторимый стиль</span>
                        <span class="hero-feature">Постоянное обновление ассортимента</span>
                        <span class="hero-feature">Удобство и высокое качество</span>
                        <span class="hero-feature">Приятные цены</span>
                    </div>
                </div>
                {"<div class='hero-image-wrap'><img class='hero-image' src='" + hero_img + "' alt='Рыбалка и кемпинг — винтажная иллюстрация'></div>" if hero_img else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Перейти в каталог", type="primary", key="hero_catalog"):
        navigate("catalog")


def _escape(text) -> str:
    return html.escape(str(text)) if text is not None else ""


def render_product_card_html(row) -> str:
    image_path = get_image_path(row.get("category", ""))
    img_uri = _image_to_data_uri(image_path) if image_path.exists() else ""
    test_info = format_test_info(row.to_dict() if hasattr(row, "to_dict") else row)
    meta = _escape(row.get("category", ""))
    if test_info:
        meta += f" · {_escape(test_info)}"

    return f"""
    <div class="product-card">
        <img class="product-card-img" src="{img_uri}" alt="{_escape(row['name'])}">
        <div class="product-card-body">
            <div class="product-card-name">{_escape(row['name'])}</div>
            <div class="product-card-desc">{_escape(truncate_text(row.get('description', '')))}</div>
            <div class="product-card-meta">{meta}</div>
            <div class="product-card-price">{row['price']:.0f} <span>руб.</span></div>
        </div>
    </div>
    """


def render_cart_contents(cart: list[dict]):
    """Список товаров в корзине без разорванных HTML-обёрток."""
    for i, item in enumerate(cart):
        meta = _escape(item.get("category", ""))
        test = format_test_info(item)
        if test:
            meta += f" · {_escape(test)}"

        cols = st.columns([4, 1, 1])
        with cols[0]:
            st.markdown(
                f"""
                <div class="cart-item">
                    <div class="cart-item-name">{_escape(item['name'])}</div>
                    <div class="cart-item-meta">{meta}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f'<div class="cart-item-price">{item["price"]:.0f} ₽</div>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            if st.button("Удалить", key=f"cart_del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

    total = sum(item["price"] for item in cart)
    st.markdown(
        f'<div class="cart-total">Итого: {total:.0f} ₽</div>',
        unsafe_allow_html=True,
    )


def render_product_detail(item, image_path: Path | None = None):
    """Карточка товара — один HTML-блок, без разорванных div."""
    test_info = format_test_info(item.to_dict() if hasattr(item, "to_dict") else item)
    test_html = f'<p class="product-detail-test"><strong>{_escape(test_info)}</strong></p>' if test_info else ""

    img_html = ""
    if image_path and image_path.exists():
        img_uri = _image_to_data_uri(image_path)
        img_html = f'<img class="product-detail-image" src="{img_uri}" alt="{_escape(item["name"])}">'

    st.markdown(
        f"""
        <div class="product-detail-page">
            <div class="product-detail-media">{img_html}</div>
            <div class="product-detail">
                <h2 class="product-detail-title">{_escape(item['name'])}</h2>
                <p class="product-detail-category"><strong>Категория:</strong> {_escape(item['category'])}</p>
                {test_html}
                <div class="product-detail-price">{item['price']:.0f} ₽</div>
                <p class="product-detail-desc">{_escape(item.get('description', ''))}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pagination_controls(
    page: int,
    total_pages: int,
    total_items: int,
    per_page: int,
    key_prefix: str = "cat",
    show_per_page: bool = True,
):
    start_item = (page - 1) * per_page + 1 if total_items else 0
    end_item = min(page * per_page, total_items)

    if show_per_page:
        top1, top2, top3 = st.columns([1, 2, 1])
        with top1:
            selected_per_page = st.selectbox(
                "На странице",
                [8, 12, 16, 24],
                index=[8, 12, 16, 24].index(per_page) if per_page in [8, 12, 16, 24] else 1,
                key=f"{key_prefix}_per_page",
            )
            if selected_per_page != st.session_state.get("catalog_per_page"):
                st.session_state.catalog_per_page = selected_per_page
                st.session_state.catalog_page = 1
                st.rerun()
        with top2:
            if total_items:
                st.markdown(
                    f"<div style='text-align:center;padding-top:0.4rem;'>"
                    f"Показано <b>{start_item}–{end_item}</b> из <b>{total_items}</b> · "
                    f"Страница <b>{page}</b> из <b>{total_pages}</b>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.markdown(
            f"<div style='text-align:center;margin-bottom:0.5rem;'>"
            f"Страница <b>{page}</b> из <b>{total_pages}</b>"
            f"</div>",
            unsafe_allow_html=True,
        )

    nav1, nav2, nav3, nav4, nav5 = st.columns([1, 1, 2, 1, 1])
    with nav1:
        if st.button("⏮ Первая", disabled=page <= 1, key=f"{key_prefix}_first", use_container_width=True):
            st.session_state.catalog_page = 1
            st.rerun()
    with nav2:
        if st.button("← Назад", disabled=page <= 1, key=f"{key_prefix}_prev", use_container_width=True):
            st.session_state.catalog_page = page - 1
            st.rerun()
    with nav3:
        page_input = st.number_input(
            "Номер страницы",
            min_value=1,
            max_value=total_pages,
            value=page,
            step=1,
            key=f"{key_prefix}_page_input",
            label_visibility="collapsed",
        )
        if page_input != page:
            st.session_state.catalog_page = int(page_input)
            st.rerun()
    with nav4:
        if st.button("Вперёд →", disabled=page >= total_pages, key=f"{key_prefix}_next", use_container_width=True):
            st.session_state.catalog_page = page + 1
            st.rerun()
    with nav5:
        if st.button("Последняя ⏭", disabled=page >= total_pages, key=f"{key_prefix}_last", use_container_width=True):
            st.session_state.catalog_page = total_pages
            st.rerun()


def render_product_grid(df: pd.DataFrame, key_prefix: str = "grid"):
    if df.empty:
        st.info("Товары не найдены.")
        return

    cols_per_row = 4
    rows = [df.iloc[i : i + cols_per_row] for i in range(0, len(df), cols_per_row)]

    for row_idx, chunk in enumerate(rows):
        cols = st.columns(cols_per_row)
        for col_idx, (_, item) in enumerate(chunk.iterrows()):
            with cols[col_idx]:
                st.markdown(render_product_card_html(item), unsafe_allow_html=True)
                pid = int(item["id"])
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Купить", key=f"{key_prefix}_buy_{pid}_{row_idx}_{col_idx}", use_container_width=True):
                        st.session_state.cart.append({
                            "id": pid,
                            "name": item["name"],
                            "price": float(item["price"]),
                            "category": item.get("category", ""),
                            "test_min": item.get("test_min"),
                            "test_max": item.get("test_max"),
                        })
                        st.toast(f"{item['name']} добавлен в корзину")
                        st.rerun()
                with b2:
                    if st.button("Подробнее", key=f"{key_prefix}_view_{pid}_{row_idx}_{col_idx}", use_container_width=True):
                        navigate("product", selected_product_id=pid)


def render_recognized_block(recognized: dict):
    if not recognized:
        return

    has_data = any([
        recognized.get("target_fish"),
        recognized.get("category_intent"),
        recognized.get("is_bank_fishing"),
        recognized.get("is_ultralight"),
        recognized.get("is_heavy"),
        recognized.get("is_budget"),
        recognized.get("is_premium"),
        recognized.get("test_min") is not None,
        recognized.get("test_max") is not None,
        recognized.get("min_price") is not None,
        recognized.get("max_price") is not None,
    ])
    if not has_data:
        return

    lines = []
    if recognized.get("category_intent"):
        lines.append(f"<b>Тип товара:</b> {recognized['category_intent']}")
    if recognized.get("target_fish"):
        lines.append(f"<b>Целевая рыба:</b> {recognized['target_fish'].capitalize()}")
    if recognized.get("is_bank_fishing"):
        lines.append("<b>Тип ловли:</b> Береговая")
    if recognized.get("is_ultralight"):
        lines.append("<b>Стиль:</b> Ультралайт / лёгкая ловля")
    if recognized.get("is_heavy"):
        lines.append("<b>Стиль:</b> Мощная / трофейная ловля")
    if recognized.get("is_budget"):
        lines.append("<b>Бюджет:</b> Недорогие варианты")
    if recognized.get("is_premium"):
        lines.append("<b>Сегмент:</b> Премиум")

    tmin = recognized.get("test_min")
    tmax = recognized.get("test_max")
    if tmin is not None or tmax is not None:
        if tmin and tmax:
            lines.append(f"<b>Тест:</b> {tmin}–{tmax} г")
        elif tmin:
            lines.append(f"<b>Тест:</b> от {tmin} г")
        elif tmax:
            lines.append(f"<b>Тест:</b> до {tmax} г")

    if recognized.get("min_price") is not None:
        lines.append(f"<b>Бюджет:</b> от {recognized['min_price']} ₽")
    if recognized.get("max_price") is not None:
        lines.append(f"<b>Бюджет:</b> до {recognized['max_price']} ₽")

    st.markdown(
        f"""
        <div class="recognized-box">
            <h4>Распознано системой</h4>
            {"<br>".join(lines)}
        </div>
        """,
        unsafe_allow_html=True,
    )